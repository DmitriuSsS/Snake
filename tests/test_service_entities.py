import unittest

from game.service_entities.queue import Queue
from game.service_entities.vector import Vector


class TestVector(unittest.TestCase):
    def test_eq(self):
        v1 = Vector(1, 2)
        v2 = Vector(1, 2)
        v3 = Vector(2, 3)

        self.assertTrue(v1 == v2)
        self.assertFalse(v1 == v3)
        self.assertFalse(v1 == 0)

    def test_mul(self):
        v = Vector(1, 2)
        result = v * 3

        self.assertEqual([3, 6], [result.x, result.y])

    def test_add(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        result = v1 + v2

        self.assertEqual([4, 6], [result.x, result.y])

    def test_hash(self):
        v1 = Vector(1, 2)
        v2 = Vector(0, 0)

        self.assertEqual(hash(v1), hash(v1))
        self.assertNotEqual(hash(v1), hash(v2))

    def test_init(self):
        v = Vector(1, 2)
        self.assertEqual([1, 2], [v.x, v.y])

    def test_str(self):
        v = Vector(0, 1)
        self.assertEqual('(0, 1)', str(v))


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
        for i in range(5):
            self.queue.enqueue(i)

    def test_get_head_and_tail(self):
        self.assertEqual(0, self.queue.head)
        self.assertEqual(4, self.queue.tail)

        q = Queue()
        self.assertTrue(q.head == q.tail is None)

    def test_enqueue(self):
        self.queue.enqueue(0)
        self.assertEqual(0, self.queue.tail)

    def test_dequeue(self):
        head = self.queue.head
        self.assertEqual(head, self.queue.dequeue())

        q = Queue()
        self.assertRaises(ValueError, q.dequeue)

    def test_get_len(self):
        self.assertEqual(5, len(self.queue))

        q = Queue()
        self.assertEqual(0, len(q))

    def test_iter(self):
        i = 0
        for item in self.queue:
            self.assertEqual(i, item)
            i += 1

    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue(1)
        self.assertEqual(1, q.dequeue())

        q.enqueue(1)
        q.enqueue(4)
        self.assertEqual(1, q.dequeue())
        self.assertEqual(4, q.dequeue())



