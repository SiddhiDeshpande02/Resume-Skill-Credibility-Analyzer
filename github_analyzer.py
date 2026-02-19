"""
GitHub profile and repository analysis
"""
import requests
import re
from datetime import datetime
from config import GITHUB_ANALYSIS


class GitHubAnalyzer:
    def __init__(self):
        """Initialize GitHub analyzer"""
        self.max_repos = GITHUB_ANALYSIS['max_repos']
    
    def extract_username_from_url(self, github_url):
        """Extract GitHub username from URL"""
        pattern = r'github\.com/([a-zA-Z0-9_-]+)'
        match = re.search(pattern, github_url)
        return match.group(1) if match else None
    
    def analyze_profile(self, github_url):
        """
        Analyze GitHub profile
        Returns profile statistics and repository information
        """
        try:
            username = self.extract_username_from_url(github_url)
            if not username:
                return None
            
            # Fetch user profile
            user_response = requests.get(
                f'https://api.github.com/users/{username}',
                timeout=10
            )
            
            if user_response.status_code != 200:
                return None
            
            user_data = user_response.json()
            
            # Fetch repositories
            repos_response = requests.get(
                f'https://api.github.com/users/{username}/repos',
                params={'sort': 'updated', 'per_page': self.max_repos},
                timeout=10
            )
            
            if repos_response.status_code != 200:
                return None
            
            repos_data = repos_response.json()
            
            # Analyze repositories
            repo_analysis = self._analyze_repositories(repos_data)
            
            profile_analysis = {
                'username': username,
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'created_at': user_data.get('created_at', ''),
                'bio': user_data.get('bio', ''),
                'repository_analysis': repo_analysis,
                'profile_url': github_url
            }
            
            return profile_analysis
            
        except Exception as e:
            print(f"Error analyzing GitHub profile: {str(e)}")
            return None
    
    def _analyze_repositories(self, repos_data):
        """Analyze repositories for technical depth"""
        languages = {}
        topics = []
        total_stars = 0
        total_forks = 0
        recent_activity = []
        
        for repo in repos_data:
            # Language statistics
            language = repo.get('language')
            if language:
                languages[language] = languages.get(language, 0) + 1
            
            # Topics
            repo_topics = repo.get('topics', [])
            topics.extend(repo_topics)
            
            # Stars and forks
            total_stars += repo.get('stargazers_count', 0)
            total_forks += repo.get('forks_count', 0)
            
            # Recent activity
            updated_at = repo.get('updated_at', '')
            if updated_at:
                recent_activity.append({
                    'name': repo.get('name', ''),
                    'updated_at': updated_at,
                    'description': repo.get('description', ''),
                    'stars': repo.get('stargazers_count', 0)
                })
        
        # Sort languages by count
        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        
        # Count unique topics
        unique_topics = list(set(topics))
        
        # Sort recent activity
        recent_activity.sort(key=lambda x: x['updated_at'], reverse=True)
        
        return {
            'total_analyzed': len(repos_data),
            'languages': dict(sorted_languages[:5]),  # Top 5 languages
            'topics': unique_topics[:10],  # Top 10 topics
            'total_stars': total_stars,
            'total_forks': total_forks,
            'recent_repos': recent_activity[:5],  # Top 5 recent repos
            'activity_level': self._calculate_activity_level(len(repos_data), total_stars)
        }
    
    def _calculate_activity_level(self, repo_count, stars):
        """Calculate GitHub activity level"""
        if repo_count >= 10 and stars >= 50:
            return 'High'
        elif repo_count >= 5 and stars >= 10:
            return 'Moderate'
        elif repo_count >= 1:
            return 'Low'
        else:
            return 'None'
    
    def extract_skills_from_github(self, github_analysis):
        """
        Extract skills from GitHub analysis
        Returns list of skills found with evidence
        """
        if not github_analysis:
            return []
        
        skills = []
        repo_analysis = github_analysis.get('repository_analysis', {})
        
        # Extract skills from languages
        languages = repo_analysis.get('languages', {})
        for language, count in languages.items():
            skills.append({
                'skill': language,
                'evidence': f"Used in {count} repositories",
                'source': 'GitHub Languages'
            })
        
        # Extract skills from topics
        topics = repo_analysis.get('topics', [])
        for topic in topics:
            skills.append({
                'skill': topic.title(),
                'evidence': 'Mentioned in repository topics',
                'source': 'GitHub Topics'
            })
        
        return skills
