import applescript
import logging


class CalendarClient():
    """Class that handles applescript requests to Calendar app
    """

    def __init__(self, calendar_name: str) -> None:
        """Constructor

        Args:
            calendar_name (str): calendar name
        """
        self.name = calendar_name

    def __repr__(self) -> str:
        return f"calendar {self.name}"

    def add_event(self, title: str, start_date: str, end_date: str, start_time: str, end_time: str) -> str:
        """Adds an event to Calendar
        Summary is set to `title` and we define the start datetime and end datetime with the provided arguments

        Args:
            title (str): title of notion card. Will be used for the calendar summary
            start_date (str) : format `%Y-%m-%d`
            end_date (str) : format `%Y-%m-%d`
            start_time (str) : format `%H:%M:%S`
            end_time (str) : format `%H:%M:%S`

        Returns:
            str : Id of the newly created event
        """
        y, m, d = start_date.split('-')
        cmd = f'set theStartDate to date "{y}-{m}-{d}"'

        h, m, s = start_time.split(':')
        set_start_hour = f"""
        set hours of theStartDate to {h}
        set minutes of theStartDate to {m}
        set seconds of theStartDate to {s}
        """
        cmd += f'{set_start_hour}'

        y, m, d = end_date.split('-')
        set_end_date = f"""
        set theEndDate to date "{y}-{m}-{d}"
        """
        cmd += f'{set_end_date}'

        h, m, s = end_time.split(':')
        set_end_hour = f"""
        set hours of theEndDate to {h}
        set minutes of theEndDate to {m}
        set seconds of theEndDate to {s}
        """
        cmd += f'{set_end_hour}'

        cmd += f"""
        tell application "Calendar"
            tell calendar "{self.name}"
                make new event with properties {{summary:"{title}", start date:theStartDate, end date:theEndDate}}
            end tell
        end tell
        """

        r = applescript.run(cmd)

        if r.out:
            event_id = r.out.split()[2]
            logging.info(f"{title} added to {self.name} calendar")
            return event_id
        else:
            logging.error(
                f"failed to add {title} to {self.name} calendar. Applescript error : {r.err}")
            raise Exception(
                f"error while creating an event in {self.name} calendar")

    def delete_event(self, id: str) -> None:
        """Remove event with id from Calendar

        Args:
            id (str) : id of the event to remove
        """
        cmd = f"""
        tell application "Calendar"
            tell calendar "{self.name}"
            delete event id "{id}"
            save
            end tell
        end tell
        """
        r = applescript.run(cmd)
        if r.err:
            logging.error(
                f"failed to delete event {id}. Applescript error : {r.err}")
            raise Exception(r.err)
        else:
            logging.info(f"event {id} removed")
