import time
import math
from EmployeePresent import EmployeePresent

#Timeunits to handle an order (now seconds)
TIMEUNIT = 1

class Employee:
    def __init__(self, id, first_name, last_name, workload, occupied=False):
        """
        Initialises a new employee.
        :param id: The id of the employee.
        :param first_name: The first name of the empoyee.
        :param last_name: The last name of the employee.
        :param workload: The workload that the employee can handle.
        :param occupied: If the employee is processing an order
        """
        self.id = id
        self.firstName = first_name
        self.lastName = last_name
        self.workload = workload
        self.occupied = occupied
        self.workDay = None
        #TODO add to datastructure for employees

    def __del__(self):
        """
        Deletes an employee.
        :return: True if the employee was deleted. False if not.
        """
        self.id = None
        self.firstName = None
        self.lastName = None
        self.workload = None
        self.occupied = None
        self.workDay = None
        #TODO remove from datastructure for employees
        return True

    def get_id(self):
        """
        Returns the employee's id.
        :return: The id of the employee.
        """
        return self.id

    def get_name(self):
        """
        Returns the employee's name.
        :return: The name of the employee.
        """
        return self.firstName + " " + self.lastName

    def get_workload(self):
        """
        Returns the workload of the employee.
        :return: The workload of this employee.
        """
        return self.workload

    def set_load(self, load):
        """
        Sets the workload of the employee to a new value.
        :param load: The new workload.
        """
        self.workload(load)

    def setWorkday(self, workday):
        """

        :param workday:
        :return:
        """
        self.workDay = workday

    def process(self, order):
        """
        Handles an order with a certain workload.
        :param order: The order that needs to be processed.
        """
        self.occupied = True
        length = math.ceil(self.workload / order.getLoad())
        time.sleep(length)
        self.workDay.putBackOnStack(self)
        self.occupied = False
