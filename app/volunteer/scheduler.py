from datetime import datetime, timedelta
from sqlalchemy import and_, or_, func
from app.models import User, VolunteerShift, VolunteerMetrics, Event
from app import db, cache

class VolunteerScheduler:
    def __init__(self):
        self.weights = {
            'seniority': 0.4,
            'reliability': 0.3,
            'availability': 0.2,
            'preference': 0.1
        }
    
    @cache.memoize(timeout=300)
    def calculate_priority_score(self, volunteer_id, shift_datetime, role):
        """Calculate priority score for volunteer assignment"""
        metrics = VolunteerMetrics.query.filter_by(volunteer_id=volunteer_id).first()
        if not metrics:
            return 0
            
        # Base score from volunteer metrics
        score = (
            metrics.seniority_score * self.weights['seniority'] +
            metrics.reliability_score * self.weights['reliability']
        )
        
        # Availability score based on existing commitments
        conflicts = VolunteerShift.query.filter(
            VolunteerShift.volunteer_id == volunteer_id,
            VolunteerShift.start_time <= shift_datetime,
            VolunteerShift.end_time >= shift_datetime
        ).count()
        
        availability_score = 1.0 if conflicts == 0 else 0.0
        score += availability_score * self.weights['availability']
        
        # Role preference score (can be customized based on volunteer preferences)
        preference_score = self._calculate_role_preference(volunteer_id, role)
        score += preference_score * self.weights['preference']
        
        return score
    
    def _calculate_role_preference(self, volunteer_id, role):
        """Calculate role preference based on historical assignments"""
        total_shifts = VolunteerShift.query.filter_by(
            volunteer_id=volunteer_id
        ).count()
        
        role_shifts = VolunteerShift.query.filter_by(
            volunteer_id=volunteer_id,
            role=role
        ).count()
        
        return role_shifts / total_shifts if total_shifts > 0 else 0.5
    
    def assign_shifts(self, event_id, required_roles):
        """Assign volunteers to shifts based on priority scores"""
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found")
            
        assignments = []
        for role, count in required_roles.items():
            # Get all eligible volunteers
            eligible_volunteers = User.query.join(VolunteerMetrics).filter(
                User.role.in_(['volunteer', 'admin']),
                User.is_active == True
            ).all()
            
            # Calculate priority scores for each volunteer
            volunteer_scores = []
            for volunteer in eligible_volunteers:
                score = self.calculate_priority_score(
                    volunteer.id, 
                    event.start_datetime,
                    role
                )
                volunteer_scores.append((volunteer, score))
            
            # Sort by priority score
            volunteer_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Assign shifts to top-scoring volunteers
            for i in range(min(count, len(volunteer_scores))):
                volunteer, score = volunteer_scores[i]
                shift = VolunteerShift(
                    event_id=event_id,
                    volunteer_id=volunteer.id,
                    role=role,
                    start_time=event.start_datetime,
                    end_time=event.end_datetime,
                    priority_score=score
                )
                db.session.add(shift)
                assignments.append(shift)
        
        db.session.commit()
        return assignments
    
    def update_volunteer_metrics(self, volunteer_id):
        """Update volunteer metrics based on historical performance"""
        metrics = VolunteerMetrics.query.filter_by(volunteer_id=volunteer_id).first()
        if not metrics:
            metrics = VolunteerMetrics(volunteer_id=volunteer_id)
            db.session.add(metrics)
        
        # Calculate total volunteer hours
        completed_shifts = VolunteerShift.query.filter_by(
            volunteer_id=volunteer_id,
            status='completed'
        ).all()
        
        total_hours = sum(
            (shift.end_time - shift.start_time).total_seconds() / 3600
            for shift in completed_shifts
        )
        
        # Calculate reliability score
        total_shifts = VolunteerShift.query.filter_by(volunteer_id=volunteer_id).count()
        cancelled_shifts = VolunteerShift.query.filter_by(
            volunteer_id=volunteer_id,
            status='cancelled'
        ).count()
        
        reliability = 1.0 - (cancelled_shifts / total_shifts if total_shifts > 0 else 0)
        
        # Update seniority score (normalized based on total hours)
        max_hours = db.session.query(func.max(VolunteerMetrics.total_hours)).scalar() or 1
        seniority = total_hours / max_hours
        
        # Update metrics
        metrics.total_hours = total_hours
        metrics.reliability_score = reliability
        metrics.seniority_score = seniority
        metrics.last_updated = datetime.utcnow()
        
        db.session.commit()
        return metrics
    
    def get_volunteer_recommendations(self, event_id, role):
        """Get AI-driven volunteer recommendations for a specific role"""
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found")
            
        # Get historical shift data for similar events
        similar_events = Event.query.filter(
            Event.event_type == event.event_type,
            Event.id != event_id
        ).all()
        
        # Analyze successful shift patterns
        successful_shifts = VolunteerShift.query.filter(
            VolunteerShift.event_id.in_([e.id for e in similar_events]),
            VolunteerShift.role == role,
            VolunteerShift.status == 'completed'
        ).all()
        
        # Calculate success metrics for each volunteer
        volunteer_success = {}
        for shift in successful_shifts:
            if shift.volunteer_id not in volunteer_success:
                volunteer_success[shift.volunteer_id] = {
                    'shifts': 0,
                    'total_hours': 0
                }
            
            hours = (shift.end_time - shift.start_time).total_seconds() / 3600
            volunteer_success[shift.volunteer_id]['shifts'] += 1
            volunteer_success[shift.volunteer_id]['total_hours'] += hours
        
        # Sort volunteers by success metrics
        recommended_volunteers = sorted(
            volunteer_success.items(),
            key=lambda x: (x[1]['shifts'], x[1]['total_hours']),
            reverse=True
        )
        
        return [User.query.get(vid) for vid, _ in recommended_volunteers[:5]]
