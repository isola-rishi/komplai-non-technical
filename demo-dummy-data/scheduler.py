"""
Komplai Demo Pipeline - Scheduler
Runs pipeline every Monday at 10:00 AM IST
"""

import schedule
import time
from datetime import datetime
import sys
import os

sys.path.append('/home/claude/komplai_demo_pipeline')

from main_pipeline import KomplaiDataPipeline


def run_weekly_pipeline():
    """Run the weekly pipeline"""
    print(f"\n{'='*70}")
    print(f"⏰ SCHEDULED RUN TRIGGERED")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    try:
        pipeline = KomplaiDataPipeline()
        result = pipeline.run()
        
        if result['success']:
            print("\n✅ Scheduled run completed successfully\n")
        else:
            print("\n❌ Scheduled run failed\n")
            
    except Exception as e:
        print(f"\n❌ Scheduled run error: {e}\n")


def main():
    """Main scheduler loop"""
    print("\n" + "="*70)
    print("  KOMPLAI DEMO PIPELINE SCHEDULER")
    print("="*70)
    print(f"\n⏰ Schedule: Every Monday at 10:00 AM IST")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Schedule the job
    schedule.every().monday.at("10:00").do(run_weekly_pipeline)
    
    # Show next run
    next_run = schedule.next_run()
    if next_run:
        print(f"📆 Next run: {next_run.strftime('%A, %B %d, %Y at %H:%M:%S')}")
    
    print(f"\n🔄 Status: Active (Press Ctrl+C to stop)")
    print("="*70 + "\n")
    
    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 Scheduler stopped by user")
        print("="*70 + "\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
