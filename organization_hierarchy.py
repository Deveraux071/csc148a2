"""Assignment 2: Organization Hierarchy
You must NOT use list.sort() or sorted() in your code.

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in an organization's hierarchy.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Sophia Huynh
"""
from __future__ import annotations
from typing import List, Optional, Union, TextIO, Tuple

# Complete the merge() function and the Employee and Organization classes
# according to their docstrings.
# Go through client_code.py to find additional methods that you must
# implement.
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.

# You must NOT use list.sort() or sorted() in your code.
# Write and make use of the merge() function instead.


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    final_lst = []
    final_lst.extend(lst1)
    for item in lst2:
        i = 0
        ref = len(final_lst)
        while i < len(final_lst):
            if item < final_lst[i]:
                final_lst.insert(i, item)
                break
            else:
                i += 1
        if len(final_lst) == ref:
            final_lst.append(item)
    return final_lst


class Employee:
    """An Employee: an employee in an organization.

    === Public Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.

    === Private Attributes ===
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - eid > 0
    - Within an organization, each eid only appears once. Two Employees cannot
      share the same eid.
    - salary > 0
    - 0 <= rating <= 100
    """
    eid: int
    name: str
    position: str
    salary: float
    rating: int
    _superior: Optional[Employee]
    _subordinates: List[Employee]

    # === TASK 1 ===
    def __init__(self, eid: int, name: str, position: str,
                 salary: float, rating: int) -> None:
        """Initialize this Employee with the ID <eid>, name <name>,
        position <position>, salary <salary> and rating <rating>.

        >>> e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e.eid
        1
        >>> e.rating
        50
        """
        self.eid = eid
        self.name = name
        self.position = position
        self.salary = salary
        self.rating = rating
        self._superior = None
        self._subordinates = []

    def __lt__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        less than <other>'s eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1 < e2
        True
        """
        if other is None:
            return False
        else:
            return self.eid < other.eid

    def get_direct_subordinates(self) -> List[Employee]:
        """Return a list of the direct subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].name
        'Emma Ployee'
        """
        final_lst = []
        for emp in self._subordinates:
            final_lst = merge(final_lst, [emp])
        return final_lst

    def get_all_subordinates(self) -> List[Employee]:
        """Return a list of all of the subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_all_subordinates()[0].name
        'Emma Ployee'
        >>> e3.get_all_subordinates()[1].name
        'Sue Perior'
        """
        if len(self._subordinates) == 0:
            return []
        else:
            final_lst = self.get_direct_subordinates()
            for emp in self.get_direct_subordinates():
                final_lst = merge(final_lst, emp.get_all_subordinates())
            return final_lst

    def get_organization_head(self) -> Employee:
        """Return the head of the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_organization_head().name
        'Bigg Boss'
        """
        if self._superior is None:
            return self
        else:
            return self._superior.get_organization_head()

    def get_superior(self) -> Optional[Employee]:
        """Returns the superior of this Employee or None if no superior exists.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_superior() is None
        True
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().name
        'Sue Perior'
        """
        if self._superior is None:
            return None
        else:
            return self._superior

    # Task 1: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def become_subordinate(self, superior: Union[Employee, None]) -> None:
        """Set this Employee's superior to <superior> and becomes a direct
        subordinate of <superior>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().eid
        2
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.become_subordinate(None)
        >>> e1.get_superior() is None
        True
        >>> e2.get_direct_subordinates()
        []
        """
        if self._superior is not None:
            self._superior._subordinates.remove(self)
        self._superior = superior
        if superior is None:
            pass
        elif len(superior._subordinates) == 0:
            superior._subordinates.append(self)
        else:
            to_insert = [self]
            superior._subordinates = merge(superior._subordinates, to_insert)

    def remove_subordinate_id(self, eid: int) -> None:
        """Remove the subordinate with the eid <eid> from this Employee's list
        of direct subordinates.

        Does NOT change the employee with eid <eid>'s superior.

        Pre-condition: This Employee has a subordinate with eid <eid>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e2.remove_subordinate_id(1)
        >>> e2.get_direct_subordinates()
        []
        >>> e1.get_superior() is e2
        True
        """

        for item in self._subordinates:
            if item.eid == eid:
                self._subordinates.remove(item)

    def add_subordinate(self, subordinate: Employee) -> None:
        """Add <subordinate> to this Employee's list of direct subordinates.

        Does NOT change subordinate's superior.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e2.add_subordinate(e1)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.get_superior() is None
        True
        """
        self._subordinates = merge(self._subordinates, [subordinate])

    def get_employee(self, eid: int) -> Optional[Employee]:
        """Returns the employee with ID <eid> or None if no such employee exists
        as a subordinate of this employee.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_employee(1) is e1
        True
        >>> e1.get_employee(1) is e1
        True
        >>> e2.get_employee(3) is None
        True
        """
        if self.eid == eid:
            return self
        elif len(self._subordinates) == 0:
            return None
        else:
            for emp in self._subordinates:
                if emp.eid == eid:
                    return emp
                if emp.get_employee(eid) is not None:
                    return emp.get_employee(eid)
            return None

    def get_employees_paid_more_than(self, amount: float) -> List[Employee]:
        """Get all subordinates of this employee that have a salary higher than
        <amount> (including this employee, if this employee's salary is higher
        than <amount>).

        Employees must be returned in increasing order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than_10000 = e3.get_employees_paid_more_than(10000)
        >>> len(more_than_10000) == 2
        True
        >>> more_than_10000[0].name
        'Sue Perior'
        >>> more_than_10000[1].name
        'Bigg Boss'
        """
        if self.salary > amount and len(self._subordinates) == 0:
            return [self]
        elif self.salary < amount and len(self._subordinates) == 0:
            return []
        else:
            final_lst = []
            if self.salary > amount:
                final_lst = merge(final_lst, [self])
            for emp in self._subordinates:
                final_lst = merge(final_lst,
                                  emp.get_employees_paid_more_than(amount))
            return final_lst

    def get_higher_paid_employees(self) -> List[Employee]:
        """
        Returns a list of all employees paid higher than <self>.
        """
        head = self.get_organization_head()
        to_search = merge([head], head.get_all_subordinates())
        final_lst = []
        for item in to_search:
            if item.salary > self.salary:
                final_lst = merge(final_lst, [item])
        return final_lst

    def get_closest_common_superior(self, eid: int) -> Employee:
        """Returns the closest common superior of <self> and the employee with
        id <eid>.
        """
        if eid == self.eid:
            return self
        else:
            ref = self.get_organization_head().get_employee(eid)
            if self in ref.get_all_subordinates():
                return ref
            else:
                return self.get_closest_common_superior(ref.get_superior().eid)

    # === TASK 2 ===
    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1.get_department_name()
        'Department'
        """
        if self._superior is None:
            return ''
        else:
            return self._superior.get_department_name()

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department, Company'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department, Company'
        >>> e3.get_position_in_hierarchy()
        'CEO, Company'
        """
        if self._superior is None:
            return self.position
        else:
            final_str = self.position
            temp = self.get_superior().get_position_in_hierarchy()
            remove_len = len(self.get_superior().position) + 2
            if temp[remove_len:] != '':  # new
                final_str = final_str + ', ' + temp[remove_len:]
            return final_str.strip()

    # === TASK 3 ===
    # Task 3: Helper methods
    #         While not called by the client_code, this method may be helpful
    #         to you and will be tested. You can (and should) call this in
    #         the other methods that you implement.
    def get_department_leader(self) -> Optional[Employee]:
        """Return the leader of this Employee's department. If this Employee is
        not in a department, return None.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_department_leader().name
        'Sue Perior'
        >>> e2.get_department_leader().name
        'Sue Perior'
        """
        if isinstance(self, Leader):
            return self
        elif self._superior is None:
            return None
        else:
            if isinstance(self._superior, Leader):
                return self._superior
            else:
                return self._superior.get_department_leader()

    def change_department_leader(self) -> Employee:
        """Changes the leader of <self>'s department to a leader object which
        has the same info as self and department name of the department leader
        and returns the new head of organization if changing the leader causes
        a change in the head, otherwise, returns the same head again.
        If self is currently a leader or does not belong to a department,
        do nothing.
        """
        if self.get_department_leader() is not None:
            replaced = self.get_department_leader()
            original_head = self.get_organization_head()
            leader = Leader(self.eid, self.name, self.position,
                            self.salary, self.rating,
                            self.get_department_leader().
                            get_department_name())
            for sub in self.get_direct_subordinates():
                sub.become_subordinate(leader)
            self._superior.remove_subordinate_id(self.eid)
            if replaced._superior is not None:
                leader.become_subordinate(replaced.get_superior())
                replaced.become_subordinate(leader)
                return leader.get_organization_head()
            else:
                original_head.become_subordinate(leader)
                return leader.get_organization_head()
        else:
            return self.get_organization_head()

    def become_leader(self, dept_name: str) -> Leader:
        """Changes the leader of <dept_name> to a leader class with
        the same info as self and the department name of the department head.
        If self is already a leader, the department name gets updated to
        <dept_name>.
        >>> e1 = Employee(1, 'Jan', 'boss', 111, 11)
        >>> e1.become_leader('comp').eid
        1
        >>> e2 = Employee(2, 'Mike', 'emp', 22, 44)
        >>> e2.become_subordinate(e1)
        >>> e2.become_leader('region').eid
        2
        >>> e2.get_direct_subordinates()
        []
        >>> e2.get_all_subordinates()
        []
        >>> isinstance(e1.get_all_subordinates()[0], Leader)
        True
        >>> len(e1.get_all_subordinates()) == 1
        True
        """
        superior = self.get_superior()
        leader = Leader(self.eid, self.name, self.position,
                        self.salary, self.rating,
                        dept_name)
        for sub in self.get_direct_subordinates():
            sub.become_subordinate(leader)
        if superior is not None:
            superior.remove_subordinate_id(self.eid)
            leader.become_subordinate(superior)
            return leader
        else:
            for sub in self._subordinates:
                self.remove_subordinate_id(sub.eid)
            leader.become_subordinate(self)
            self._subordinates = []  # new
            leader._superior = None
            return leader

    def become_employee(self) -> Employee:
        """<self> becomes an employee. This is an abstract method since an
        employee cannot be made an employee (by preconditions)
        """
        raise NotImplementedError

    # Part 4: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def get_highest_rated_subordinate(self) -> Employee:
        """Return the subordinate of this employee with the highest rating.

        Pre-condition: This Employee has at least one subordinate.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Sue Perior'
        >>> e1.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Emma Ployee'
        """
        sub_rating_list = []
        rating_list = []
        temp_list = []
        for sub in self.get_direct_subordinates():
            sub_rating_list.append([sub, sub.rating])
            rating_list.append(sub.rating)

        maxi = max(rating_list)
        for item in sub_rating_list:
            if maxi == item[1]:
                temp_list = merge(temp_list, [item[0]])
        return temp_list[0]

    def swap_up(self) -> Employee:
        """Swap this Employee with their superior. Return the version of this
        Employee that is contained in the Organization (i.e. if this Employee
        becomes a Leader, the new Leader version is returned).

        Pre-condition: self is not the head of the Organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> new_e1 = e1.swap_up()
        >>> isinstance(new_e1, Leader)
        True
        >>> new_e2 = new_e1.get_direct_subordinates()[0]
        >>> isinstance(new_e2, Employee)
        True
        >>> new_e1.position
        'Manager'
        >>> new_e1.eid
        1
        >>> e3.get_direct_subordinates()[0] is new_e1
        True
        """
        if isinstance(self._superior, Leader):
            new_leader = Leader(self.eid, self.name, self._superior.position,
                                self._superior.salary,
                                self.rating,
                                self._superior.get_department_name())
            return self.swap_up_helper(new_leader)
        else:
            new_emp = Employee(self.eid, self.name, self._superior.position,
                               self._superior.salary, self.rating)
            return self.swap_up_helper(new_emp)

    def swap_up_helper(self, employee: Employee) -> Employee:
        """Helper for the swap_up function.
        """
        for sub in self._superior.get_direct_subordinates():
            if sub.eid == self.eid:
                emp = Employee(self._superior.eid, self._superior.name,
                               self.position, self.salary,
                               self._superior.rating)
                for i in self.get_direct_subordinates():
                    i.become_subordinate(emp)
                emp.become_subordinate(employee)
            else:
                sub.become_subordinate(employee)
            self._superior.remove_subordinate_id(sub.eid)

        if self._superior._superior is not None:
            self._superior._superior. \
                remove_subordinate_id(self._superior.eid)
            employee.become_subordinate(self._superior._superior)
        else:
            org = Organization(self._superior)
            org.set_head(employee)
        return employee

    def obtain_subordinates(self, ids: List[int]) -> Employee:
        """<self> obtains all the Employees with ids in <ids>. The subordinates
        of employees with eid in <ids> become the subordinates of their previous
        superior's superior. If the head od the organization is made the
        subordinate of self, the highest rated direct subordinate of the head
        becomes the new head.
        """
        if len(ids) == 0:
            return self.get_organization_head()
        else:
            org = Organization(self.get_organization_head())
            if self.get_organization_head().eid not in ids:
                for item in ids:
                    emp = org.get_employee(item)
                    sup = emp.get_superior()
                    _obtain_sub_helper(emp, sup)
                    emp.become_subordinate(self)
                return self.get_organization_head()
            else:
                if ids[0] == self.get_organization_head().eid:
                    original_head = self.get_organization_head()  # id1
                    new_head = \
                        self.get_organization_head()\
                            .get_highest_rated_subordinate()
                    org.set_head(new_head)
                    emp = org.get_employee(self.eid)
                    original_head.become_subordinate(emp)
                else:
                    emp = org.get_employee(ids[0])
                    sup = emp.get_superior()
                    _obtain_sub_helper(emp, sup)
                    emp.become_subordinate(self)
                ids = ids[1:]
                return self.obtain_subordinates(ids)


def _obtain_sub_helper(emp: Employee, sup: Employee) -> None:
    """Helper for obtain_subordinates. Helps in adding the subordinates of <emp>
    into <sup>"""
    for sub in emp.get_direct_subordinates():
        sub.become_subordinate(sup)
        emp.remove_subordinate_id(sub.eid)


class Organization:
    """An Organization: an organization containing employees.

    === Private Attributes ===
    _head:
        The head of the organization.

    === Representation Invariants ===
    - _head is either an Employee (or subclass of Employee) or None (if there
      are no Employees).
    - No two Employees in an Organization have the same eid.
    """
    _head: Optional[Employee]

    # === TASK 1 ===
    def __init__(self, head: Optional[Employee] = None) -> None:
        """Initialize this Organization with the head <head>.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        """
        self._head = head

    def get_employee(self, eid: int) -> Optional[Employee]:
        """
        Return the employee with id <eid>. If no such employee exists, return
        None.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o.add_employee(e1)
        >>> o.get_employee(1) is e1
        True
        >>> o.get_employee(2) is None
        True
        """
        if self._head is None:
            return None
        elif self._head.eid == eid:
            return self._head
        else:
            return self._head.get_employee(eid)

    def add_employee(self, employee: Employee, superior_id: int = None) -> None:
        """Add <employee> to this organization as the subordinate of the
        employee with id <superior_id>.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.get_head() is e2
        True
        >>> o.add_employee(e1, 2)
        >>> o.get_employee(1) is e1
        True
        >>> e1.get_superior() is e2
        True
        """
        if self._head is None and employee is not None:
            self._head = employee
        elif superior_id is None or superior_id <= 0:
            self._head.become_subordinate(employee)
            self._head = employee
        else:
            sub = merge([self._head], self._head.get_all_subordinates())
            for emp in sub:
                if emp.eid == superior_id:
                    employee.become_subordinate(emp)

    def get_average_salary(self, position: Optional[str] = None) -> float:
        """Returns the average salary of all employees in the organization with
        the position <position>.

        If <position> is None, this returns the average salary of all employees.

        If there are no such employees, return 0.0

        >>> o = Organization()
        >>> o.get_average_salary()
        0.0
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.get_average_salary()
        15000.0
        """
        if self._head is None:
            return 0.0
        elif position is None:
            to_search = merge([self._head], self._head.get_all_subordinates())
            total = 0.0
            i = 0
            while i < len(to_search):
                total += to_search[i].salary
                i += 1
            return total/i
        else:
            to_search = merge([self._head], self._head.get_all_subordinates())
            total = 0.0
            i = 0
            j = 0
            while i < len(to_search):
                if to_search[i].position == position:
                    total += to_search[i].salary
                    j += 1
                i += 1
            if j == 0:
                return 0.0
            else:
                return total/i

    def get_employees_with_position(self, position: str) -> List[Employee]:
        """Returns a list of all employees in the organization with
        position <position>."""
        final_lst = []
        for item in merge([self._head], self._head.get_all_subordinates()):
            if item.position == position:
                final_lst = merge(final_lst, [item])
        return final_lst

    def get_next_free_id(self) -> int:
        """Get the next free id in the organization. i.e The lowest id which
        is not  assigned  to any Employee."""
        if self._head is None:
            return 1
        else:
            id_list = []
            to_search = merge([self._head], self._head.get_all_subordinates())
            for i in to_search:
                id_list.append(i.eid)
            smallest = 1
            while smallest in id_list:
                smallest += 1
            return smallest

    # === TASK 3 ===

    def set_head(self, new_head: Employee) -> None:
        """Sets the head of the organization to <new_head>. <new_head> also
        picks up all the subordinates of the old head."""
        new_head.become_subordinate(None)
        if self._head is None:
            self._head = new_head
        else:
            for sub in self._head.get_direct_subordinates():
                if sub != new_head:
                    sub.become_subordinate(new_head)
            self._head = new_head

    # === TASK 4 ===

    def get_head(self) -> Employee:
        """Return the head of the organization."""
        return self._head

    def fire_employee(self, eid: int) -> None:
        """Remove the employee with id <eid> from the organization and:
        (1) make all of the subordinates of the employee with id <eid>
        as the subordinates of the superior of the employee with id <eid>
        if it exists. OR
        (2) IF no superior of self exists (if employee with id <eid> is
        organization head), make the highest rated direct subordinate the
        head of the organization and all the other direct subordinates of
        employee with id <eid> become the direct subordinates of the new head.
        Pre-condition: there is an employee with the eid <eid> in
        self.current_organization.
        """
        if self._head.eid != eid:
            emp = self.get_employee(eid)
            sup = emp.get_superior()
            for sub in emp.get_direct_subordinates():
                sub.become_subordinate(sup)
            sup.remove_subordinate_id(eid)
        else:
            new_head = \
                self._head.get_highest_rated_subordinate()
            self.set_head(new_head)

    def fire_lowest_rated_employee(self) -> None:
        """Fires the lowest rated employee in the organization."""
        if self._head is not None:
            self._fire_lowest_rated_employee_helper()

    def _fire_lowest_rated_employee_helper(self) -> None:
        """Helper for fire_lowest_rated_employee."""
        emp = self._head.get_all_subordinates()
        final_lst = []
        temp_lst = []
        if len(emp) == 0:
            self._head = None
        else:
            emp = merge(emp, [self._head])
            minimum = emp[0].rating
            emp = emp[1:]
            for i in emp:
                temp_lst = merge(temp_lst, [i.rating])
            if min(temp_lst) < minimum:
                minimum = min(temp_lst)
            emp = merge([self._head], self._head.get_all_subordinates())
            for item in emp:
                if item.rating == minimum:
                    final_lst = merge(final_lst, [item])
            to_fire = final_lst[0]
            self.fire_employee(to_fire.eid)

    def fire_under_rating(self, rating: int) -> None:
        """Fires all the employees whose ratings are under <rating>."""
        if self._head is not None:
            self._fire_under_rating_helper(rating)

    def _fire_under_rating_helper(self, rating: int) -> None:
        """Helper for fire_under_rating."""
        low_rating_list = []
        rating_list = []
        final_lst = []
        emp_list = merge([self._head], self._head.get_all_subordinates())
        for item in emp_list:
            if item.rating < rating:
                low_rating_list = merge(low_rating_list, [item])
                if item.rating not in rating_list:
                    rating_list = merge(rating_list, [item.rating])

        for item in rating_list:
            for emp in low_rating_list:
                if emp.rating == item:
                    final_lst = merge(final_lst, [emp])

        for item in final_lst:
            self.fire_employee(item.eid)

    def promote_employee(self, eid: int) -> None:
        """Promote the employee  with id <eid> until its superior has a higher
        rating than itself."""
        emp = self.get_employee(eid)
        if emp is not None and emp.get_superior() is not None:
            if emp.rating >= emp.get_superior().rating:
                new_emp = emp.swap_up()
                self._head = new_emp.get_organization_head()
                self.promote_employee(new_emp.eid)


# === TASK 2: Leader ===
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.
#
# After the completion of Task 2, you should be able to run organization_ui.py,
# though not all of the buttons will work.


class Leader(Employee):
    """A subclass of Employee. The leader of a department in an organization.

    === Private Attributes ===
    _department_name:
        The name of the department this Leader is the head of.

    === Inherited Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).
    # # my private attribute:
    # _list_of_positions: Gives a list of positions used
    # in get_positions_in_heirarchy

    === Representation Invariants ===
    - All Employee RIs are inherited.
    - Department names are unique within an organization.
    """
    _department_name: str

    # === TASK 2 ===
    def __init__(self, eid: int, name: str, position: str, salary: float,
                 rating: int, department: str) -> None:
        """Initialize this Leader with the ID <eid>, name <name>, position
        <position>, salary <salary>, rating <rating>, and department name
        <department>.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e2.name
        'Sue Perior'
        >>> e2.get_department_name()
        'Department'
        """
        Employee.__init__(self, eid, name, position, salary, rating)
        self._department_name = department

    def get_department_name(self) -> str:
        """Returns the name of the department this Leader is in. If the
        Leader is not part of a department, return an empty string.
        """
        return self._department_name

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Leader's position in the
        organization.
        """
        final_str = self.position
        final_str = final_str + ', ' + self._department_name
        if self.get_superior() is not None:
            if self.get_superior().get_department_leader() is None:
                return final_str.strip()
            else:
                temp = self.get_superior().get_position_in_hierarchy()
                remove_len = len(self.get_superior().position) + 2
                final_str = final_str + ', ' + temp[remove_len:]
                return final_str.strip()
        else:
            return final_str.strip()

    def get_department_employees(self) -> List[Employee]:
        """Returns a list of all the employees in the department headed by
        <self>."""
        return merge([self], self.get_all_subordinates())

    # === TASK 3 ===
    def become_employee(self) -> Employee:
        """<self> becomes an employee object with the same data as before
        except the department name."""
        emp = Employee(self.eid, self.name, self.position, self.salary,
                       self.rating)
        for sub in self.get_direct_subordinates():
            sub.become_subordinate(emp)
        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)
            emp.become_subordinate(self._superior)
            return emp
        else:
            for sub in self.get_direct_subordinates():
                self.remove_subordinate_id(sub.eid)
            emp.become_subordinate(self)
            for sub in self.get_direct_subordinates():
                sub._superior = None
                self._subordinates = []
            return emp

    def change_department_leader(self) -> Employee:
        """Makes <self> the department leader of the department it is in.
        But since this is already a leader, does not do anything and only
        returns the head of the organization."""
        return self.get_organization_head()

    def become_leader(self, dept_name: str) -> Leader:
        """Changes the leader of <dept_name> to a leader class with
        the same info as self and the department name of the department head.
        If self is already a leader, the department name gets updated to
        <dept_name>.
        """
        if self._department_name != dept_name:
            self._department_name = dept_name
        return self

    # === TASK 4 ===

    def swap_up(self) -> Employee:
        """Swap this Employee with their superior. Return the version of this
        Employee that is contained in the Organization (i.e. if this Employee
        becomes a Leader, the new Leader version is returned).

        Pre-condition: self is not the head of the Organization."""
        if isinstance(self._superior, Leader):
            new_leader = Leader(self.eid, self.name, self._superior.position,
                                self._superior.salary,
                                self.rating,
                                self._superior.get_department_name())
            return self.swap_up_helper(new_leader)
        else:
            new_emp = Employee(self.eid, self.name, self._superior.position,
                               self._superior.salary, self.rating)
            return self.swap_up_helper(new_emp)

    def swap_up_helper(self, employee: Employee) -> Employee:
        """Helper for the swap_up function."""
        for sub in self._superior.get_direct_subordinates():
            if sub.eid == self.eid:
                leader = Leader(self._superior.eid, self._superior.name,
                                self.position, self.salary,
                                self._superior.rating, self._department_name)
                for i in self.get_direct_subordinates():
                    i.become_subordinate(leader)
                leader.become_subordinate(employee)
            else:
                sub.become_subordinate(employee)
            self._superior.remove_subordinate_id(sub.eid)

        if self._superior._superior is not None:
            self._superior._superior. \
                remove_subordinate_id(self._superior.eid)
            employee.become_subordinate(self._superior._superior)
        else:
            org = Organization(self._superior)
            org.set_head(employee)
        return employee


# === TASK 5 ===
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

class DepartmentSalaryTree:
    """A DepartmentSalaryTree: A tree representing the salaries of departments.
    The salaries considered only consist of employees directly in a department
    and not in any of their subdepartments.

    Do not change this class.

    === Public Attributes ===
    department_name:
        The name of the department that this DepartmentSalaryTree represents.
    salary:
        The average salary of the department that this DepartmentSalaryTree
        represents.
    subdepartments:
        The subdepartments of the department that this DepartmentSalaryTree
        represents.
    """
    department_name: str
    salary: float
    subdepartments: [DepartmentSalaryTree]

    def __init__(self, department_name: str, salary: float,
                 subdepartments: List[DepartmentSalaryTree]) -> None:
        """Initialize this DepartmentSalaryTree with the department name
        <department_name>, salary <salary>, and the subdepartments
        <subdepartments>.

        >>> d = DepartmentSalaryTree('Department', 30000, [])
        >>> d.department_name
        'Department'
        """
        self.department_name = department_name
        self.salary = salary
        self.subdepartments = subdepartments[:]


def create_department_salary_tree(organization: Organization) -> \
        Optional[DepartmentSalaryTree]:
    """Return the DepartmentSalaryTree corresponding to <organization>.

    If <organization> has no departments, return None.

    Pre-condition: If there is at least one department in <organization>,
    then the head of <organization> is also a Leader.

    >>> o = Organization()
    >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    >>> o.add_employee(e2)
    >>> o.add_employee(e1, 2)
    >>> o.add_employee(e3)
    >>> dst = create_department_salary_tree(o)
    >>> dst.department_name
    'Company'
    >>> dst.salary
    50000.0
    >>> dst.subdepartments[0].department_name
    'Department'
    >>> dst.subdepartments[0].salary
    15000.0
    """
    if not isinstance(organization.get_head(), Leader):
        return None
    else:
        head = organization.get_head()
        direct_employees = head.get_direct_subordinates()
        head_department = head.get_department_name()
        add = head.salary
        count = 1
        sub_departments = []
        for employee in direct_employees:
            if isinstance(employee, Leader):
                sub_departments.append(_department_salary_tree(employee))
            else:
                value1, value2 = _get_salary(employee)
                add += value1
                count += value2
        avg_salary = add / count
        salary_tree = DepartmentSalaryTree(head_department, avg_salary,
                                           sub_departments)
        return salary_tree


def _department_salary_tree(employee: Employee) -> \
        Union[DepartmentSalaryTree, List[DepartmentSalaryTree]]:
    """Return the DepartmentSalaryTree of the organization under employee
    <employee>.
    """
    if len(employee.get_direct_subordinates()) == 0 and \
            isinstance(employee, Leader):
        salary_tree = DepartmentSalaryTree(employee.get_department_name(),
                                           employee.salary, [])
        return salary_tree
    elif isinstance(employee, Leader):
        department_name = employee.get_department_name()
        lst_departments = []
        add = employee.salary
        count = 1
        for emp in employee.get_direct_subordinates():
            if isinstance(emp, Leader):
                lst_departments.append(_department_salary_tree(emp))
            else:
                lst_departments.extend(_department_salary_tree(emp))
                value1, value2 = _get_salary(emp)
                add += value1
                count += value2
        avg_salary = add / count
        salary_tree = DepartmentSalaryTree(department_name, avg_salary,
                                           lst_departments)
        return salary_tree
    else:
        lst_departments = []
        for emp in employee.get_direct_subordinates():
            if isinstance(emp, Leader):
                lst_departments.append(_department_salary_tree(emp))
            else:
                lst_departments.extend(_department_salary_tree(emp))
        return lst_departments


def _get_salary(employee: Employee) -> Tuple[float, int]:
    """Return the avg salary of the employees belonging to this department.

    Pre-condition: <employee> is a Leader.
    """
    if isinstance(employee, Leader):
        return 0, 0
    else:
        direct_employees = employee.get_direct_subordinates()
        add = employee.salary
        count = 1
        for emp in direct_employees:
            if not isinstance(emp, Leader):
                value1, value2 = _get_salary(emp)
                add += value1
                count += value2
        return add, count

# === TASK 6 ===
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.


def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.

    >>> o = create_organization_from_file(open('employees.txt'))
    >>> o.get_head().name
    'Alice'
    """
    lst_employees = []
    head = None
    for employee in file:
        employee_details = employee.split(',')
        if len(employee_details) == 7 and employee_details[5] != '':
            leader = Leader(int(employee_details[0]), employee_details[1],
                            employee_details[2], float(employee_details[3]),
                            int(employee_details[4]), employee_details[6])
            superior_id = int(employee_details[5].rstrip())
            lst_employees.append((leader, superior_id))
        elif len(employee_details) == 7 and employee_details[5] == '':
            head = Leader(int(employee_details[0]), employee_details[1],
                          employee_details[2], float(employee_details[3]),
                          int(employee_details[4]), employee_details[6])
        else:
            emp = Employee(int(employee_details[0]), employee_details[1],
                           employee_details[2], float(employee_details[3]),
                           int(employee_details[4]))
            superior_id = int(employee_details[5].rstrip())
            lst_employees.append((emp, superior_id))
    for subordinate in lst_employees:
        if subordinate[1] == head.eid:
            subordinate[0].become_subordinate(head)
    for subordinate in lst_employees:
        for superior in lst_employees:
            if subordinate[1] == superior[0].eid:
                subordinate[0].become_subordinate(superior[0])
    return Organization(head)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'doctest', 'typing',
                                   '__future__'],
        'max-args': 7})
