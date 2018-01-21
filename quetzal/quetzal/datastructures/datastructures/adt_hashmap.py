# import dll
from . import AdtDoublyLinkedList

LINEAR_PROBING = 0
QUADRATIC_PROBING = 1
SEPARATE_CHAINING = 2


class _DataNode:
    def __init__(self, search_key, data):
        """ Creates new datanode.

        :param search_key: The searchkey of the node.
        :param data: The data of the node.
        """
        self.search_key = search_key
        self.data = data

    def __del__(self):
        self.search_key = None
        self.data = None


class AdtHashMap:
    def __init__(self, length, collision_type):
        """ Initialises a new hashmap with a certain length and collision type.

        :param length: The length of the hashmap.
        :param collision_type: The way to solve a collision.
        """
        self.lijst = None
        # If the params are valid, create the main variables
        self._create_hashmap(length, collision_type)
        self.length = length
        self.collision_type = collision_type

    def __del__(self):
        """
        Deletes the hashmap.
        """
        self.lijst = None
        self.length = 0
        self.collision_type = None

    def _create_hashmap(self, length, collision_type):
        """ Create a new hashmap.

        :param length: The length of the table.
        :param collision_type: The way to solve a collision.
        """
        # Input validation
        if 0 > collision_type > 2:
            raise ValueError("Invalid collision type!")

        if length <= 0:
            raise ValueError("Invalid length!")

        # Creating map
        self.lijst = []
        for i in range(length):
            self.lijst.append("")
        # If linked lists are used, fill every position with an empty link
        if collision_type == 2:
            for i in range(length):
                new_link = AdtDoublyLinkedList()
                self.lijst[i] = new_link

    def is_empty(self):
        """ Checks if the list is empty.

        :return: True if list is empty, false otherwise
        """
        for item in self.lijst:
            if self.collision_type == SEPARATE_CHAINING:
                if not item.is_empty():
                    return False
            elif item != "":
                return False
        return True

    def __setitem__(self, search_key, data):
        """ Inserts a new element in the table.

        :param search_key: The new item to insert.
        :param data: The data that needs to be stored.
        """
        # Calculate address and make datanode
        adres = self._calculate_address(search_key)
        new_node = _DataNode(search_key, data)
        # Collision can't occur with separate chaining
        if self.collision_type == SEPARATE_CHAINING:
            self.lijst[adres].insertBeginning(new_node)
        else:
            # Check if a collision occurs
            if self.lijst[adres] != "":
                self._solve_collision(adres, new_node)
            else:
                self.lijst[adres] = new_node

    def _calculate_address(self, search_key):
        """ Calculates the adres with the hashfunction.

        :param search_key: The key to be used in the function
        :return: The adres calculated by the hash function.
        """
        adres = 0
        if isinstance(search_key, str):
            adres = len(search_key) % self.length
        elif isinstance(search_key, int):
            adres = search_key % self.length
        return adres

    def __getitem__(self, search_key):
        """ Returns an item from the hashmap.

        :param search_key: The item to search for and return.
        :raise KeyError if the searchkey is not in the hashmap.
        :return: The data linked with the search_key
        """
        if self.is_empty():
            raise KeyError("Hashmap is empty!")
        pos = self._find(search_key)
        if pos is None:
            raise KeyError("Hashmap does not contain given search key!")
        else:
            return self.lijst[pos].data

    def __delitem__(self, search_key):
        """ Deletes item from hashmap.

        :param search_key: Key from the node that needs to be deleted.
        :raise KeyError if the searchkey is not in the hashmap.
        """
        if self.is_empty():
            raise KeyError("Hashmap is empty!")
        pos = self._find(search_key)
        if pos is None:
            raise KeyError("Hashmap does not contain given search key!")
        else:
            self.lijst[pos] = ""

    def __contains__(self, search_key):
        """ Finds data with a given searchkey in the map.

        :param search_key: Key from the node that has to be found.
        :return: True if the searchkey is in the map, false otherwise.
        """
        pos = self._find(search_key)
        if pos is None:
            return False
        else:
            return True

    def _find(self, search_key):
        """ Finds the position with a given searchkey.

        :param search_key: The key to find in the hashmap
        :return: The position of the data or None
        """
        adres = self._calculate_address(search_key)
        if self.collision_type == SEPARATE_CHAINING:
            pos = self._seperate_chaining_search(adres, search_key)
        elif self.collision_type == LINEAR_PROBING:
            pos = self._linear_probing_search(adres, search_key)
        else:
            pos = self._quadratic_probing_search(adres, search_key)
        return pos

    def _solve_collision(self, adres, data):
        """ Solves a collision by choosing from one of the methods.

        :param adres: Address that caused collision
        :param data: The item to be inserted.
        """
        if self.collision_type == LINEAR_PROBING:
            self._linear_probing(adres, data)
        elif self.collision_type == QUADRATIC_PROBING:
            self._quadratic_probing(adres, data)

    def _linear_probing(self, adres, node):
        """ Solve a collision with linear probing.

        :param adres: Address that caused collision.
        :param node: The node (with searchkey and data) to be inserted.
        :raise MemoryError if the hashmap is full.
        """
        current_adres = adres
        count = 0
        while True:
            # Insert element
            if self.lijst[current_adres] == "":
                self.lijst[current_adres] = node
                break

            current_adres += 1
            count += 1

            if count == self.length:
                raise MemoryError("Hashmap is full!")

            # Make sure to keep looping over the list
            if current_adres == self.length:
                current_adres = 0

    def _linear_probing_search(self, adres, key):
        """ Searches in the map for a given key.

        :param adres: The address that as calculated for that searchkey.
        :param key: The searchkey of the item that needs to be found.
        :return: The node if the key matched an element from the list, None otherwise.
        """
        count = 0
        while True:
            # Search through the list for the searchkey
            if self.lijst[adres] != "":
                if self.lijst[adres].search_key == key:
                    return adres
            adres += 1
            count += 1
            if count == self.length:
                return None

            # Make sure to keep looping over the list
            if adres == self.length:
                adres = 0

    def _quadratic_probing(self, adres, node):
        """ Solve a collision with quadratic probing.

        :param adres: Address that caused collision.
        :param node: The item to be inserted.
        :return: Indicates whether the collision was solved. True if it was,
        false if it couldn't solve the collision.
        """
        current_adres = adres
        # We put i on 2 because 0**2 is already checked before increment
        i = 1
        count = 0
        while True:
            # Search through the list for the searchkey
            if self.lijst[current_adres] == "":
                self.lijst[current_adres] = node
                break
            current_adres = (adres + i**2)
            i += 1
            count += 1
            # Check if the whole list was checked
            if count == self.length:
                return None
            # Make sure to keep looping over the list
            if current_adres >= self.length:
                current_adres = current_adres % self.length

    def _quadratic_probing_search(self, adres, key):
        """ Searches in the map for a given key.

        :param adres: The address that as calculated for that searchkey.
        :param key: The searchkey of the item that needs to be found.
        :return: True if the node is found, false otherwise.
        """
        current_address = adres
        i = 1
        counter = 0
        while True:
            if self.lijst[current_address] != "":
                if self.lijst[current_address].search_key == key:
                    return current_address
            current_address = (adres + i**2)
            i += 1
            counter += 1
            # Check if the whole list was checked
            if counter == self.length:
                return None
            # Make sure to keep looping over the list
            if current_address >= self.length:
                current_address = current_address % self.length

    def _seperate_chaining(self, adres, data, delete):
        """ Solve a collision with separate chaining.

        :param adres: Address that caused collision.
        :param data: The item to be inserted.
        :param delete: Indicates if the algorithm has to delete or not.
        :return: Indicates whether the collision was solved or the item found. True if it was,
        false if it couldn't solve the collision.
        """
        if search:
            table = self.lijst[adres]
            length = table.get_length()
            current_link = table.head
            counter = 0
            while counter != length:
                if current_link.item.search_key == data:
                    if delete:
                        table.delete(counter)
                    else:
                        return current_link.item
                else:
                    current_link = current_link.next
                    counter += 1
            return False
        else:
            self.lijst[adres].insert_beginning(data)
            return True

    def _seperate_chaining_search(self, adres, key):
        """

        :param adres:
        :param key:
        :return:
        """
        pass