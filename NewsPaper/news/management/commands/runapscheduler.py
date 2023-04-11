from django.core.management.base import BaseCommand

from ...scheduler import create_scheduler


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        try:
            created_scheduler = create_scheduler()
            logger = created_scheduler['logger']
            scheduler = created_scheduler['scheduler']

            logger.info("Starting scheduler...")
            print("Starting scheduler...")
            scheduler.start()
            print(" after Starting scheduler...")
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            print("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
            print("Scheduler shut down successfully!")