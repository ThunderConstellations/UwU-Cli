#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Infinite Mode for UwU-CLI
Provides continuous AI assistance until task completion
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import threading

class InfiniteMode:
    def __init__(self, cursor_controller=None):
        self.cursor_controller = cursor_controller
        self.active_jobs = {}
        self.job_history = {}
        self.job_counter = 0
        self.running = False
        
    def start_infinite_job(self, user_id: str, plan: str = "") -> str:
        """Start infinite mode for a user"""
        try:
            job_id = f"infinite_{user_id}_{int(time.time())}"
            
            # Create job entry
            self.active_jobs[job_id] = {
                'user_id': user_id,
                'plan': plan or "Continue working on current task until completion",
                'start_time': datetime.now().isoformat(),
                'status': 'active',
                'iterations': 0,
                'last_prompt': None,
                'last_result': None,
                'completed_tasks': [],
                'errors': []
            }
            
            # Start background task in a separate thread
            thread = threading.Thread(target=self._run_infinite_loop, args=(job_id,))
            thread.daemon = True
            thread.start()
            
            return f"🚀 Infinite mode started! Job ID: {job_id}\n\nPlan: {plan or 'Continue until completion'}"
        except Exception as e:
            return f"❌ Failed to start infinite mode: {str(e)}"
    
    def stop_infinite_job(self, user_id: str) -> str:
        """Stop infinite mode for a user"""
        try:
            stopped_jobs = []
            for job_id, job in list(self.active_jobs.items()):
                if job['user_id'] == user_id and job['status'] == 'active':
                    job['status'] = 'stopped'
                    job['end_time'] = datetime.now().isoformat()
                    stopped_jobs.append(job_id)
                    
                    # Move to history
                    self.job_history[job_id] = job
                    del self.active_jobs[job_id]
            
            if stopped_jobs:
                return f"🛑 Stopped {len(stopped_jobs)} infinite job(s): {', '.join(stopped_jobs)}"
            else:
                return "ℹ️ No active infinite jobs found for this user."
        except Exception as e:
            return f"❌ Failed to stop infinite mode: {str(e)}"
    
    def _run_infinite_loop(self, job_id: str):
        """Run the infinite loop for a job"""
        try:
            job = self.active_jobs[job_id]
            max_iterations = 50  # Prevent infinite loops
            
            while job['status'] == 'active' and job['iterations'] < max_iterations:
                # Build continuation prompt
                if job['iterations'] == 0:
                    prompt = f"Start working on: {job['plan']}"
                else:
                    prompt = f"Continue working on: {job['plan']}. This is iteration {job['iterations'] + 1}."
                
                # Send to Cursor AI if available
                if self.cursor_controller:
                    try:
                        result = self.cursor_controller.send_prompt(prompt)
                        job['last_result'] = result
                    except Exception as e:
                        job['errors'].append(f"Iteration {job['iterations'] + 1}: {str(e)}")
                else:
                    job['last_result'] = f"Simulated result for: {prompt}"
                
                # Update job status
                job['iterations'] += 1
                job['last_prompt'] = prompt
                
                # Check if we should continue
                if not self._should_continue(job_id):
                    break
                
                # Wait before next iteration
                time.sleep(5)  # 5 second delay
            
            # Mark job as completed
            if job_id in self.active_jobs:
                job = self.active_jobs[job_id]
                job['status'] = 'completed'
                job['end_time'] = datetime.now().isoformat()
                
                # Move to history
                self.job_history[job_id] = job
                del self.active_jobs[job_id]
                
        except Exception as e:
            if job_id in self.active_jobs:
                job = self.active_jobs[job_id]
                job['status'] = 'error'
                job['error'] = str(e)
                job['end_time'] = datetime.now().isoformat()
    
    def _should_continue(self, job_id: str) -> bool:
        """Check if job should continue"""
        if job_id not in self.active_jobs:
            return False
        
        job = self.active_jobs[job_id]
        return job['status'] == 'active'
    
    def get_job_status(self, user_id: str) -> str:
        """Get status of user's infinite jobs"""
        try:
            user_jobs = []
            for job_id, job in self.active_jobs.items():
                if job['user_id'] == user_id:
                    user_jobs.append(job)
            
            if not user_jobs:
                return "ℹ️ No active infinite jobs for this user."
            
            status = f"Active Infinite Jobs ({len(user_jobs)}):\n"
            for job in user_jobs:
                status += f"• {job['plan'][:50]}... (Iteration {job['iterations']})\n"
            
            return status
        except Exception as e:
            return f"❌ Failed to get job status: {str(e)}"
    
    def get_job_history(self, user_id: str) -> str:
        """Get history of user's completed infinite jobs"""
        try:
            user_history = []
            for job_id, job in self.job_history.items():
                if job['user_id'] == user_id:
                    user_history.append(job)
            
            if not user_history:
                return "ℹ️ No completed infinite jobs for this user."
            
            history = f"Completed Infinite Jobs ({len(user_history)}):\n"
            for job in user_history[:5]:  # Show last 5
                duration = "Unknown"
                if 'end_time' in job and 'start_time' in job:
                    try:
                        start = datetime.fromisoformat(job['start_time'])
                        end = datetime.fromisoformat(job['end_time'])
                        duration = str(end - start).split('.')[0]
                    except:
                        pass
                
                history += f"• {job['plan'][:40]}... ({job['status']}, {duration})\n"
            
            return history
        except Exception as e:
            return f"❌ Failed to get job history: {str(e)}"
    
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up old completed jobs"""
        try:
            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
            jobs_to_remove = []
            
            for job_id, job in self.job_history.items():
                if 'end_time' in job:
                    try:
                        end_time = datetime.fromisoformat(job['end_time']).timestamp()
                        if end_time < cutoff_time:
                            jobs_to_remove.append(job_id)
                    except:
                        pass
            
            for job_id in jobs_to_remove:
                del self.job_history[job_id]
            
            return f"🧹 Cleaned up {len(jobs_to_remove)} old jobs"
        except Exception as e:
            return f"❌ Cleanup failed: {str(e)}" 