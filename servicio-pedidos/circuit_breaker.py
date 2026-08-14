import time 

class CircuitBreaker:

    def __init__(self, max_failure=3, recovery_timeout=20):
        self.max_failure = max_failure
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.state = "CLOSED"
        self.opened_at = None

    # Funcion que decide si se permite realizar una peticion
    def can_request (self):

        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":

            elapsed_time = time.monotonic () - self.opened_at

            if elapsed_time >= self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True

            return False

        return True

    # Funcion que registra los fallos 
    def record_failure  (self):

        self.failure_count += 1

        if self.failure_count >= self.max_failure:
            self.state = "OPEN"
            self.opened_at = time.monotonic ()


    # Funcion que cierra y reinicia el circuito si todo esta correcto
    def record_success (self):

        self.state = "CLOSED"
        self.failure_count = 0
        self.opened_at = None


    

        
