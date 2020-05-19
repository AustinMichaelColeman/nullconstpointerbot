from nullconstpointer.commands.icommand import ICommand


SECONDS_PER_MINUTE = 60
MINUTE = "minute"
SECOND = "second"


class TimerCommand(ICommand):
    def __init__(self, processor, caller_user, time_minutes):
        self.processor = processor
        self.caller_user = caller_user
        self.time_seconds = 0
        if time_minutes is not None:
            self.time_seconds = int(time_minutes) * SECONDS_PER_MINUTE

    def add_plural(self, word, count):
        if count > 1 or count == 0:
            word += "s"
        return word

    def remove_ending_space(self, message):
        return message[:-1]

    def time_remaining(self):
        minutes, seconds = divmod(
            self.processor.get_time_remaining(), SECONDS_PER_MINUTE
        )

        minute_grammar = self.add_plural(MINUTE, minutes)
        second_grammar = self.add_plural(SECOND, seconds)

        message = ""
        if minutes != 0:
            message += f"{minutes} {minute_grammar} "

        if seconds != 0:
            message += f"{seconds} {second_grammar} "

        return self.remove_ending_space(message)

    def success_time_remaining(self, time_remaining, current_user, next_level):
        return (
            f"There is {time_remaining} remaining for level "
            f"{next_level} submitted by {current_user}"
        )

    def success_starting_new_timer_stopping_previous(self):
        return (
            f"Previous timer stopped. Starting new timer. "
            + self.success_time_remaining_message()
        )

    def success_time_expired(self, level, user):
        return f"Timer has expired for level {level} submitted by {user}"

    def success_starting_new_timer(self):
        return f"Starting new timer. {self.success_time_remaining_message()}"

    def fail_timer_not_set(self):
        return "A timer has not been set yet."

    def fail_no_current_level(self):
        return "There is no current level to time. Use !next or !random"

    def fail_enter_a_timer_value(self):
        return f"{self.caller_user}, invalid entry, please provide number."

    def start_timer(self):
        self.processor.start_timer(self.time_seconds)

    def success_time_remaining_message(self):
        return self.success_time_remaining(
            self.time_remaining(),
            self.processor.current_user,
            self.processor.next_level(),
        )

    def execute(self):
        if self.caller_user == self.processor.current_owner:
            if not self.processor.timer_has_been_set():
                if not self.time_seconds:
                    return self.fail_enter_a_timer_value()

            if not self.processor.next_level():
                return self.fail_no_current_level()

            if self.processor.timer_has_been_set():
                if not self.time_seconds:
                    if self.processor.get_time_remaining() <= 0:
                        return self.success_time_expired(
                            self.processor.next_level(), self.processor.current_user
                        )
                    return self.success_time_remaining_message()
                self.start_timer()
                return self.success_starting_new_timer_stopping_previous()

            self.start_timer()
            return self.success_starting_new_timer()

        if self.processor.timer_has_been_set():
            return self.success_time_remaining_message()

        return self.fail_timer_not_set()
