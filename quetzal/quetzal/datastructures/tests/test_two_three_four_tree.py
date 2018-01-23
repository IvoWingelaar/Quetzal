from datastructures import *
from unittest import TestCase
from random import shuffle

class TestTwoThreeFourTree(TestCase):
    def test_init_and_delete(self):
        t = AdtTwoThreeFourTree()
        self.assertTrue(t.is_empty())
        self.assertEqual(t.root, None)
        t[0] = 45
        t[1] = 10
        self.assertFalse(t.is_empty())
        self.assertNotEqual(t.root, None)

    def test_insert(self):
        t = AdtTwoThreeFourTree()
        t[10] = "10a"
        t[10] = "10b"
        t[60] = "60"
        t[10] = "10c"
        self.assertFalse(t.is_empty())
        t[30] = "30"
        t[40] = "40"
        self.assertEqual(t.root.amount, 1)
        t[70] = "70"
        self.assertEqual(t.root.amount, 1)
        t[90] = "90"
        self.assertEqual(t.root.amount, 2)
        self.assertEqual(t.root.children[0].amount, 1)
        self.assertEqual(t.root.children[1].amount, 1)
        self.assertEqual(t.root.children[2].amount, 2)
        self.assertEqual(t.root.children[3], None)

    def test_mega_fuzz(self):
        rounds = 20
        unique_insertions = 10

        print()
        for k in range(1, rounds):
            print('Fuzz round', k)

            keys = [x for x in range(1, unique_insertions)]
            shuffle(keys)

            for i in range(0, 4):
                # Duplicate the last N elements for insertion
                duplicates = keys[-10:]
                keys.extend(duplicates)
                shuffle(keys)

            # Explicitly creates duplicates of a higher multiplicity.
            duplicates = keys[-3:]
            for i in range(0, 3):
                keys.extend(duplicates)
            shuffle(keys)

            tree = AdtTwoThreeFourTree()
            # Insert all keys.
            for i in keys:
                tree[i] = i

            # Check for validity.
            #inorder_list_of_keys = [x[0] for x in rb]
            #self.assertEqual(sorted(inorder_list_of_keys), inorder_list_of_keys)

            # Check if everything can be found.
            for i in keys:
                self.assertTrue(i in tree)

            copy_of_ = list(keys)
            original = list(keys)
            shuffle(keys)

            removed = []

            for i in keys:
                del tree[i]
                original.remove(i)
                removed.append(i)

                #inorder_list_of_keys = [x[0] for x in rb]
                #self.assertEqual(sorted(inorder_list_of_keys), inorder_list_of_keys)

                # If it's still in the original, then it also must be in our tree.
                for j in original:
                    self.assertTrue(j in tree)

                for j in removed:
                    # Duplicates can be found multiple times.
                    if j in original:
                        self.assertTrue(j in tree)
                    else:
                        self.assertFalse(j in tree)
