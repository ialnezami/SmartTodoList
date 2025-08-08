import openai
import re
from datetime import datetime, timedelta
from django.conf import settings
from typing import Dict, List, Optional, Tuple


class AIService:
    """AI service for task management features"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def categorize_task(self, title: str, description: str = "") -> Dict:
        """Categorize a task based on its title and description"""
        try:
            prompt = f"""
            Categorize the following task into one of these categories:
            - personal: Personal tasks, hobbies, self-care
            - work: Work-related tasks, professional development
            - health: Health, fitness, medical appointments
            - shopping: Shopping, errands, purchases
            - finance: Financial tasks, bills, budgeting
            - education: Learning, studying, courses
            - travel: Travel planning, trips, transportation
            - home: Home maintenance, cleaning, repairs
            
            Task: {title}
            Description: {description}
            
            Return only the category name (e.g., "personal", "work", etc.)
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )
            
            category = response.choices[0].message.content.strip().lower()
            
            # Validate category
            valid_categories = ['personal', 'work', 'health', 'shopping', 'finance', 'education', 'travel', 'home']
            if category not in valid_categories:
                category = 'personal'
            
            return {
                'category': category,
                'confidence_score': 85,
                'suggested_category': category
            }
            
        except Exception as e:
            return {
                'category': 'personal',
                'confidence_score': 0,
                'suggested_category': 'personal',
                'error': str(e)
            }
    
    def suggest_priority(self, title: str, description: str = "", due_date: Optional[datetime] = None) -> Dict:
        """Suggest priority level for a task"""
        try:
            # Base priority calculation
            priority = 3  # Default medium priority
            
            # Check for urgency keywords
            urgency_keywords = ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'deadline']
            title_lower = title.lower()
            description_lower = description.lower()
            
            for keyword in urgency_keywords:
                if keyword in title_lower or keyword in description_lower:
                    priority = 5
                    break
            
            # Check due date
            if due_date:
                days_until_due = (due_date - datetime.now()).days
                if days_until_due < 0:  # Overdue
                    priority = 5
                elif days_until_due <= 1:  # Due today or tomorrow
                    priority = max(priority, 4)
                elif days_until_due <= 3:  # Due this week
                    priority = max(priority, 3)
                elif days_until_due <= 7:  # Due next week
                    priority = max(priority, 2)
            
            # AI-based priority suggestion
            prompt = f"""
            Suggest a priority level (1-5) for this task:
            - 1: Very low priority, can be done anytime
            - 2: Low priority, not urgent
            - 3: Medium priority, normal importance
            - 4: High priority, should be done soon
            - 5: Very high priority, urgent/critical
            
            Task: {title}
            Description: {description}
            Due Date: {due_date.strftime('%Y-%m-%d') if due_date else 'No due date'}
            
            Return only the number (1-5).
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.1
            )
            
            ai_priority = int(response.choices[0].message.content.strip())
            ai_priority = max(1, min(5, ai_priority))  # Ensure it's between 1-5
            
            # Combine rule-based and AI-based priority
            final_priority = max(priority, ai_priority)
            
            return {
                'priority': final_priority,
                'confidence_score': 80,
                'reasoning': f"Based on urgency keywords, due date, and AI analysis"
            }
            
        except Exception as e:
            return {
                'priority': 3,
                'confidence_score': 0,
                'reasoning': 'Default priority due to error',
                'error': str(e)
            }
    
    def parse_natural_language(self, text: str) -> Dict:
        """Parse natural language input to extract task details"""
        try:
            prompt = f"""
            Parse the following natural language task input and extract:
            1. Task title
            2. Description (if any)
            3. Due date (if mentioned)
            4. Priority level (1-5)
            5. Category
            
            Input: "{text}"
            
            Return a JSON object with these fields:
            {{
                "title": "extracted title",
                "description": "extracted description or empty string",
                "due_date": "YYYY-MM-DD HH:MM or null",
                "priority": number 1-5,
                "category": "personal/work/health/shopping/finance/education/travel/home"
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.1
            )
            
            # Parse the response (this is a simplified version)
            content = response.choices[0].message.content.strip()
            
            # Extract information using regex patterns
            title_match = re.search(r'"title":\s*"([^"]+)"', content)
            description_match = re.search(r'"description":\s*"([^"]*)"', content)
            due_date_match = re.search(r'"due_date":\s*"([^"]*)"', content)
            priority_match = re.search(r'"priority":\s*(\d+)', content)
            category_match = re.search(r'"category":\s*"([^"]+)"', content)
            
            result = {
                'title': title_match.group(1) if title_match else text,
                'description': description_match.group(1) if description_match else '',
                'due_date': due_date_match.group(1) if due_date_match and due_date_match.group(1) != 'null' else None,
                'priority': int(priority_match.group(1)) if priority_match else 3,
                'category': category_match.group(1) if category_match else 'personal'
            }
            
            return result
            
        except Exception as e:
            return {
                'title': text,
                'description': '',
                'due_date': None,
                'priority': 3,
                'category': 'personal',
                'error': str(e)
            }
    
    def estimate_duration(self, title: str, description: str = "") -> int:
        """Estimate task duration in minutes"""
        try:
            prompt = f"""
            Estimate the duration of this task in minutes:
            Task: {title}
            Description: {description}
            
            Consider:
            - Simple tasks: 15-30 minutes
            - Medium tasks: 30-120 minutes
            - Complex tasks: 2-8 hours
            - Very complex tasks: 8+ hours
            
            Return only the number of minutes.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )
            
            duration = int(response.choices[0].message.content.strip())
            return max(15, min(duration, 480))  # Between 15 minutes and 8 hours
            
        except Exception as e:
            return 30  # Default 30 minutes
    
    def get_task_suggestions(self, user_tasks: List[Dict]) -> List[Dict]:
        """Get AI-powered task suggestions based on user history"""
        try:
            if not user_tasks:
                return []
            
            # Analyze user patterns
            categories = {}
            priorities = {}
            completion_times = []
            
            for task in user_tasks:
                category = task.get('category', 'personal')
                categories[category] = categories.get(category, 0) + 1
                
                priority = task.get('priority', 3)
                priorities[priority] = priorities.get(priority, 0) + 1
                
                if task.get('status') == 'completed':
                    completion_times.append(task.get('estimated_duration', 30))
            
            # Generate suggestions based on patterns
            suggestions = []
            
            # Suggest tasks based on most common categories
            most_common_category = max(categories.items(), key=lambda x: x[1])[0] if categories else 'personal'
            
            category_suggestions = {
                'personal': ['Review personal goals', 'Plan weekend activities', 'Organize personal space'],
                'work': ['Review weekly progress', 'Plan next week', 'Update professional skills'],
                'health': ['Schedule workout', 'Plan healthy meals', 'Book medical checkup'],
                'shopping': ['Create shopping list', 'Research product reviews', 'Compare prices'],
                'finance': ['Review monthly budget', 'Pay bills', 'Update financial records'],
                'education': ['Read educational material', 'Practice new skills', 'Enroll in course'],
                'travel': ['Research destinations', 'Plan trip itinerary', 'Book accommodations'],
                'home': ['Home maintenance check', 'Organize living space', 'Plan home improvements']
            }
            
            for suggestion in category_suggestions.get(most_common_category, []):
                suggestions.append({
                    'title': suggestion,
                    'category': most_common_category,
                    'priority': 3,
                    'estimated_duration': 30,
                    'confidence_score': 70
                })
            
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            return []
    
    def optimize_schedule(self, tasks: List[Dict]) -> List[Dict]:
        """Optimize task schedule based on priority, duration, and deadlines"""
        try:
            if not tasks:
                return []
            
            # Sort tasks by priority (descending) and due date (ascending)
            sorted_tasks = sorted(tasks, key=lambda x: (
                -x.get('priority', 3),
                x.get('due_date', datetime.max) if x.get('due_date') else datetime.max
            ))
            
            # Add scheduling metadata
            current_time = datetime.now()
            for i, task in enumerate(sorted_tasks):
                task['suggested_order'] = i + 1
                task['estimated_start_time'] = current_time + timedelta(minutes=i * 30)
                
                # Estimate completion time
                duration = task.get('estimated_duration', 30)
                task['estimated_completion_time'] = task['estimated_start_time'] + timedelta(minutes=duration)
            
            return sorted_tasks
            
        except Exception as e:
            return tasks 