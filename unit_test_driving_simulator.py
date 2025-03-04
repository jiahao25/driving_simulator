import unittest

# Import your classes (assuming they are in the same file or module)
from driving_simulator import Field, CarStates, Car  # Replace `your_module` with the actual module name

class TestField(unittest.TestCase):
    def test_within_boundary(self):
        field = Field(10, 10)
        # Test within boundary
        self.assertTrue(field.within_boundary(5, 5))
        # Test on boundary
        self.assertTrue(field.within_boundary(0, 0))
        self.assertTrue(field.within_boundary(9, 9))
        # Test outside boundary
        self.assertFalse(field.within_boundary(10, 10))
        self.assertFalse(field.within_boundary(-1, -1))


class TestCarStates(unittest.TestCase):
    def setUp(self):
        # Some example states
        self.car_states = CarStates({
            'car1': [0, 0, 'N', 'moving', [], []],
            'car2': [5, 5, 'S', 'stopped', [], []]
        })

    def test_return_state(self):
        # Test returning states
        self.assertEqual(self.car_states.return_state('car1', 'x'), 0)
        self.assertEqual(self.car_states.return_state('car1', 'y'), 0)
        self.assertEqual(self.car_states.return_state('car1', 'dir'), 'N')
        self.assertEqual(self.car_states.return_state('car1', 'state'), 'moving')
        self.assertEqual(self.car_states.return_state('car2', 'state'), 'stopped')

    def test_update_state(self):
        # Test updating states
        self.car_states.update_state('car1', 'x', 1)
        self.assertEqual(self.car_states.return_state('car1', 'x'), 1)

        self.car_states.update_state('car1', 'dir', 'E')
        self.assertEqual(self.car_states.return_state('car1', 'dir'), 'E')

        self.car_states.update_state('car1', 'state', 'stopped')
        self.assertEqual(self.car_states.return_state('car1', 'state'), 'stopped')


class TestCar(unittest.TestCase):
    def setUp(self):
        # Some field and CarState values example
        self.field = Field(10, 10)
        self.car_states = CarStates({
            'car1': [0, 0, 'N', 'moving', [], []]
        })
        # Some Car state example
        self.car = Car('car1', 0, 0, 'N', ['F', 'R', 'F'], self.car_states, self.field)

    def test_move_forward(self):
        # Test moving forward within boundary
        self.car.move(0)  # First command is 'F'
        self.assertEqual(self.car_states.return_state('car1', 'x'), 0)
        self.assertEqual(self.car_states.return_state('car1', 'y'), 1)
        self.assertEqual(self.car_states.return_state('car1', 'dir'), 'N')

    def test_move_outside_boundary(self):
        # Test moving forward outside boundary
        self.car_states.update_state('car1', 'y', 9)  # Move car to the edge
        self.car.move(0)  # First command is 'F'
        # Car should not move outside the boundary
        self.assertEqual(self.car_states.return_state('car1', 'y'), 9)

    def test_turn_left(self):
        # Test turning left
        self.car.move(1)  # Second command is 'R' (right turn)
        self.assertEqual(self.car_states.return_state('car1', 'dir'), 'E')

    def test_turn_right(self):
        # Test turning right
        self.car.move(1)  # Second command is 'R' (right turn)
        self.assertEqual(self.car_states.return_state('car1', 'dir'), 'E')

    def test_collision(self):
        # Test collision logic
        # Add another car to the state
        self.car_states.car_curr_state['car2'] = [0, 1, 'N', 'moving', [], []]
        self.car.move(0)  # First command is 'F'
        # Car1 should collide with Car2 at (0, 1)
        self.assertEqual(self.car_states.return_state('car1', 'state'), 'collided')
        self.assertEqual(self.car_states.return_state('car2', 'state'), 'collided')


if __name__ == '__main__':
    unittest.main()