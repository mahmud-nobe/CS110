import unittest

from Assignments.cs110_assignment_2.Activities.Activity_Module import Activity
from Assignments.cs110_assignment_2.Activities.Queue_Module import *
from Assignments.cs110_assignment_2.Activities.Task_Module import *


class TestTask(unittest.TestCase):

    def setUp(self):
        self.task_1: Task = Task(10, "Eat bubble gum")
        self.task_2: Task = Task(15, "Eat candy")
        self.task_3: Task = Task(10, "Eat chocolate")

    def tearDown(self) -> None:
        Task.reset()

    def test_task_creation(self):
        self.assertTrue(
            self.task_1.id != self.task_2.id,
            "Each task must have a unique id"
        )
        self.assertEqual(
            self.task_1.original_duration, 10,
            "The original duration must equal that passed in instantiation"
        )
        self.assertEqual(
            self.task_1.duration, 10,
            "Remaining duration should equal duration"
        )
        self.assertEqual(
            self.task_1.description,
            "Eat bubble gum",
            "Description should be equal to that in instantiation"
        )

    def test_id(self):
        def adjust_id(task: Task, new_id: int):
            task.id = new_id

        self.assertRaises(TypeError, adjust_id, self.task_1, 5)

    def test_duration(self):
        def adjust_original_duration(task: Task, new_duration: float):
            task.original_duration = new_duration

        self.assertRaises(
            TypeError, adjust_original_duration, self.task_1, 100)

        def adjust_duration(task: Task, new_duration: float):
            task.duration = new_duration

        self.assertRaises(
            TypeError, adjust_duration, self.task_1, 100)

    def test_status(self):
        self.assertEqual(
            self.task_1.status, status.NOT_YET_STARTED,
            "The task should have not yet started")
        self.task_1.complete(2)
        self.assertTrue(
            self.task_1.is_in_progress(),
            "The task should be in progress after a certain amount of its duration has been completed"
        )
        self.task_1.complete(10)
        self.assertTrue(
            self.task_1.is_complete() and self.task_1.duration == 0,
            "The task should be completed now and its remaining duration equal to 0"
        )

        def adjust_status(task: Task, new_status: int):
            task.status = new_status

        self.assertRaises(
            TypeError, adjust_status, self.task_1, status.NOT_YET_STARTED)

    def test_comparisons(self):
        self.assertTrue(
            self.task_2 > self.task_1,
            f"Task 2 should be greater than task 3; task_2 {self.task_2.duration}, {self.task_3.duration}"
        )
        self.task_2.complete(7)
        self.assertTrue(
            self.task_3 > self.task_2,
            f"Task 3 should be greater than task 2; ; task_2 {self.task_2.duration}, {self.task_3.duration}"
        )
        self.assertTrue(
            self.task_2 < self.task_3,
            f"Task 2 should be less than task 3; ; task_2 {self.task_2.duration}, {self.task_3.duration}"
        )

    def test_dependencies(self):
        def adjust_dependency(task: Task):
            task.dependencies = {}

        self.assertRaises(
            TypeError, adjust_dependency, self.task_1)

        self.task_1.add_dependency(self.task_2, self.task_3)
        self.assertEqual(
            len(self.task_1.dependencies),
            2,
            "Task 1 should have 2 dependencies"
        )

        def adjust_dependants(task: Task):
            task.dependants = {}

        self.assertRaises(
            TypeError, adjust_dependants, self.task_1)

        self.assertTrue(
            len(self.task_2.dependants) == 1 and len(
                self.task_3.dependants) == 1,
            "Both task 2 and 3 have 1 task that depend on them"
        )

        self.task_2.complete(20)
        self.assertTrue(
            len(self.task_1.dependencies) == 1 and len(
                self.task_2.dependants) == 0,
            "Task 1 should have 1 dependency remaining and task 2 should have no dependants"
        )

        self.task_3.add_dependency(self.task_2)
        self.assertTrue(
            len(self.task_3.dependencies) == 0 and self.task_3.id not in self.task_2.dependants,
            "Since we completed task 2, we shouldn't be able to add it as a dependency"
        )

    def test_all_tasks(self):
        self.assertTrue(
            # The count of all tasks should be equal to the id of the last task instantiated
            len(Task.all_tasks()) == self.task_3.id
        )

    def test_reset(self):
        Task.reset()
        self.assertTrue(
            len(Task.all_tasks()) == 0,
            "All the tasks must be deleted and cleaned out"
        )
        task = Task(1, "Eat java beans")
        self.assertTrue(
            len(Task.all_tasks()) == 1 and task.id == 1,
            "Ensure that after a reset id's begin from the 1st one"
        )


class TestActivity(unittest.TestCase):

    def setUp(self) -> None:
        self.task_1 = Task(10, "Talking")
        self.task_2 = Task(10, "Writing")
        self.activity_1 = Activity("Meeting", self.task_1, self.task_2)
        self.activity_2 = Activity("Exercise")

    def tearDown(self) -> None:
        Task.reset()

    def test_instantiation(self):
        self.assertTrue(
            self.activity_1.name == "Meeting",
            "The name of the activity should match that it was instantiated with"
        )
        self.assertTrue(
            len(self.activity_1.tasks) == 2,
            "The activity should contain two tasks that it was instantiated with"
        )

        new_act = Activity("New")
        self.assertTrue(
            len(new_act.tasks) == 0,
            "A new activity with no task parameters should have no tasks"
        )

    def test_update_name(self):
        self.activity_1.name = "Exercise"
        self.assertTrue(
            self.activity_1.name == "Exercise",
            "The name of the activity should match that it got updated to"
        )

    def test_tasks(self):
        def adjust_tasks(activity: Task):
            activity.tasks = {}

        self.assertRaises(
            TypeError, adjust_tasks, self.activity_1)

    def test_associate_tasks(self):
        self.assertTrue(
            self.activity_1 == self.task_1.activity,
            "Activity 1 should be similar to the activity in task 1"
        )
        self.assertTrue(
            len(self.activity_2.tasks) == 0,
            "Activity should not have any tasks"
        )
        self.activity_2.add_tasks(self.task_2)
        self.assertTrue(
            len(self.activity_2.tasks) == 1,
            "Activity 2 should have 1 activity now"
        )
        self.assertTrue(
            self.task_2.activity == self.activity_2,
            "Task 2 should have activity 2 as its activity"
        )
        self.assertTrue(
            len(self.activity_1.tasks) == 1,
            "Activity 1 should now have 1 task"
        )

        task_3 = Task(5, "Eat cabbage", self.activity_1)
        self.assertTrue(
            task_3.activity == self.activity_1,
            "Task 3 should have its activity set to activity 1"
        )

        self.assertTrue(
            len(self.activity_1.tasks) == 2,
            "Activity 1 should now have 2 tasks"
        )


class TestQueues(unittest.TestCase):

    def test_heapify(self):
        A = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
        my_heap = MaxHeapq()

        for key in A:
            my_heap.heappush(key)

        for i, key in enumerate(my_heap.heap):
            if i != 0:
                self.assertTrue(
                    key <= my_heap.heap[my_heap.parent(i)]
                )
