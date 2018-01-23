from quetzal import *
from unittest import TestCase
from random import shuffle


class TestHashmap(TestCase):
    # General

    def testRetrieveEmpty(self):
        hashmap = AdtHashMap(1, 1)
        try:
            test = hashmap[0]
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

    def testDeleteEmpty(self):
        hashmap = AdtHashMap(1, 1)
        try:
            del hashmap[0]
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

    # Tests for linear probing

    def testLinearProbing(self):
        hashmap = AdtHashMap(5, 0)
        hashmap[3] = "test"
        hashmap[33] = "test2"
        self.assertEqual(hashmap.lijst[3].search_key, 3)
        self.assertEqual(hashmap.lijst[4].search_key, 33)
        hashmap["searchkey"] = "test3"
        self.assertEqual(hashmap.lijst[0].search_key, "searchkey")

    def testLinearProbingFull(self):
        hashmap = AdtHashMap(5, 0)
        hashmap[3] = "test1"
        hashmap[33] = "test2"
        hashmap[23] = "test3"
        hashmap[88] = "test4"
        hashmap[123] = "test5"
        try:
            hashmap[13] = "test6"
            self.assertTrue(False)
        except MemoryError:
            self.assertTrue(True)

    def testGetLP(self):
        hashmap = AdtHashMap(5, 0)
        hashmap[4] = "test"
        self.assertEqual(hashmap[4], "test")
        try:
            test = hashmap[5]
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

    def testDeleteLP(self):
        hashmap = AdtHashMap(5, 0)
        hashmap[5] = "test"
        del hashmap[5]
        try:
            test = hashmap[5]
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)
        self.assertTrue(hashmap.is_empty())

    def testContainsLP(self):
        hashmap = AdtHashMap(5, 0)
        hashmap[3] = "test1"
        hashmap[33] = "test2"
        hashmap[23] = "test3"
        self.assertTrue(3 in hashmap)
        self.assertTrue(33 in hashmap)
        self.assertTrue(23 in hashmap)
        self.assertFalse(56 in hashmap)

    # Tests for quadratic probing

    def testQuadraticProbing(self):
        hashmap = AdtHashMap(5, 1)
        hashmap[15] = "test"
        hashmap[25] = "test"
        hashmap[35] = "test"
        self.assertEqual(hashmap.lijst[0].search_key, 15)
        self.assertEqual(hashmap.lijst[1].search_key, 25)
        self.assertEqual(hashmap.lijst[4].search_key, 35)

    def testQuadraticProbingFull(self):
        hashmap = AdtHashMap(5, 1)
        hashmap[2] = "test"
        hashmap[7] = "test"
        hashmap[5] = "test"
        hashmap[15] = "test"
        hashmap[25] = "test"
        try:
            hashmap[35] = "test"
            self.assertTrue(False)
        except MemoryError:
            self.assertTrue(True)

    def testGetQP(self):
        hashmap = AdtHashMap(5, 1)
        hashmap[4] = "test"
        self.assertEqual(hashmap[4], "test")
        try:
            test = hashmap[5]
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

    def testDeleteQP(self):
        hashmap = AdtHashMap(5, 1)
        hashmap[5] = "test"
        del hashmap[5]
        try:
            test = hashmap[5]
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)
        self.assertTrue(hashmap.is_empty())

    def testContainsQP(self):
        hashmap = AdtHashMap(5, 0)
        hashmap[3] = "test1"
        hashmap[33] = "test2"
        hashmap[23] = "test3"
        self.assertTrue(3 in hashmap)
        self.assertTrue(33 in hashmap)
        self.assertTrue(23 in hashmap)
        self.assertFalse(56 in hashmap)

    # Tests for separate chaining

    def testSeparateChaining(self):
        hashmap = AdtHashMap(5, 2)
        hashmap[0] = "test"
        hashmap[1] = "test"
        hashmap[2] = "test"
        hashmap[3] = "test"
        hashmap[4] = "test"
        hashmap[5] = "test"
        hashmap[6] = "test"
        self.assertTrue(True)

    def testGetSC(self):
        hashmap = AdtHashMap(5, 2)
        hashmap[4] = "test"
        self.assertEqual(hashmap[4], "test")
        with self.assertRaises(KeyError):
            test = hashmap[5]

    def testDeleteSC(self):
        hashmap = AdtHashMap(5, 2)
        hashmap[5] = "test"
        del hashmap[5]
        with self.assertRaises(KeyError):
            test = hashmap[5]
        self.assertTrue(hashmap.is_empty())
        hashmap[5] = "test1"
        hashmap[15] = "test2"
        hashmap[25] = "test3"
        del hashmap[15]
        self.assertEqual(len(hashmap.lijst[0]), 2)
        del hashmap[5]
        del hashmap[25]
        self.assertTrue(hashmap.is_empty())

    def testContainsSc(self):
        hashmap = AdtHashMap(5, 2)
        hashmap[0] = "test0"
        hashmap[1] = "test1"
        hashmap[5] = "test2"
        hashmap[15] = "test3"
        hashmap[25] = "test4"
        self.assertTrue(0 in hashmap)
        self.assertTrue(15 in hashmap)
        self.assertTrue(1 in hashmap)
        del hashmap[15]
        self.assertFalse(15 in hashmap)

    # def testDot(self):
    #     hashmap = AdtHashMap(5, 2)
    #     hashmap[0] = "test"
    #     hashmap[1] = "test"
    #     hashmap[2] = "test"
    #     hashmap[3] = "test"
    #     hashmap[4] = "test"
    #     hashmap[5] = "test"
    #     hashmap[6] = "test"
    #     hashmap[0] = "test0"
    #     hashmap[1] = "test1"
    #     hashmap[5] = "test2"
    #     hashmap[15] = "test3"
    #     hashmap[25] = "test4"
    #     text = hashmap.__repr__()
    #     file = open("test1.dot", "w")
    #     file.write(text)
    #     file.close()

    def test_mega_fuzz(self):
        rounds = 20
        unique_insertions = 500

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

            tree = AdtHashMap()
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
