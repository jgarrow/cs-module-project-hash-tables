class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
    
    def __str__(self):
        return 'key: {self.key}, value: {self.value}'.format(self=self)


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity = MIN_CAPACITY):
        cpcty = capacity

        # check if the provided capacity meets the minimum capacity requirement
        if capacity < MIN_CAPACITY:
            cpcty = MIN_CAPACITY

        # Your code here
        self.capacity = cpcty
        # self.head = None
        self.hash_table = [None] * cpcty # create a hash_table list of length cpcty
        self.total_items = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Your code here
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # Your code here
        return self.total_items / self.capacity 


    # def fnv1(self, key):
    #     """
    #     FNV-1 Hash, 64-bit

    #     Implement this, and/or DJB2.
    #     """

    #     # Your code here


    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        

        Implement this, and/or FNV-1.
        """
        # Your code here
        # https://stackoverflow.com/questions/1579721/why-are-5381-and-33-so-important-in-the-djb2-algorithm                                                                                                                               
        hash = 5381
        bytes_to_hash = key.encode() 

        for byte in bytes_to_hash:
            # << is a bitwise operator; in this case, it shifts the "bits" of `hash` left by 5 
            hash = ((hash << 5) + byte)
        
        # for x in key: 
        #     # << is a bitwise operator; in this case, it shifts the "bits" of `hash` left by 5 "bits"
        #     hash = (( hash << 5) + hash) + ord(x) # hash + 33 + ord(x)
        
        return hash


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here

        idx = self.hash_index(key)
        entry = HashTableEntry(key, value)
        match = None

        # if there's already something stored at this index
        if self.hash_table[idx] is not None:
            curr_node = self.hash_table[idx]

            # look for an existing entry with the same key
            while match is None:
                if curr_node.key == key:
                    match = curr_node
                else:
                    curr_node = curr_node.next
                
                # if we reached the tail and still haven't found an existing match, break out of the loop
                if curr_node is None:
                    break

            # if we reached the end and didn't find an existing entry matching the provided key
            # add a new entry at the end
            if match is None and curr_node.next is None:
                curr_node.next = entry
                self.total_items+= 1
                self.determine_resize_type()

            # if an entry with the provided key already exists, just update its value with the provided value
            elif match is not None:
                match.value = value
            
        
        # if nothing exists as this index, just add the entry
        else:
            self.hash_table[idx] = entry
            self.total_items+= 1
            self.determine_resize_type()


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        idx = self.hash_index(key)

        if idx >= 0 and idx < self.capacity:
            # find the entry node that matches the provided key
            prev_node = None
            curr_node = self.hash_table[idx]
            match = None

            # check if any node at index exists
            if curr_node is None:
                print(f'Key {key} was not found')
                return
            else:
                # loop until we find a match for the provided key
                while match is None:
                    # check to see if there is an entry at this index whose key matches the provided key
                    if curr_node.key != key:
                        prev_node = curr_node
                        curr_node = curr_node.next
                    
                    elif curr_node.key == key:
                        match = curr_node
                    
                    # if we've reached the tail and still haven't found a match
                    if curr_node.next is None and match is None:
                        print(f'Key {key} was not found')
                        return 
                
                # if prev_node is still None and match.next is None, that means there is only 1 node at this index
                if prev_node is None and match.next is None:
                    self.hash_table[idx] = None
                elif prev_node is not None:
                    prev_node.next = match.next
                
                self.total_items-= 1
            
        else:
            print(f'Key {key} was not found')
            return
        


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here

        idx = self.hash_index(key)

        # check if the index is in range
        if idx >= 0 and idx < self.capacity:
            curr_node = self.hash_table[idx]

            # check if any node at index exists
            if curr_node is None:
                return None

            # if there's already something at this index
            while curr_node is not None:
                
                # check to see if there is an entry at this index whose key matches the provided key
                while curr_node.key is not key:
                    curr_node = curr_node.next
                
                # if we never found an entry with a matching key, return None
                if curr_node.key is not key or curr_node is None:
                    return None
                else:
                    return curr_node.value
            
        
        # otherwise return None if the index is not in range
        else:
            return None


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        self.capacity = new_capacity

        # make new array to store the current self.hash_table
        # update self.hash_table to be array of size new_capacity
        # for each item in our copy array
        # self.put(item) in our newly size self.hash_table
        # if item.next is not None
        # make sure to self.put(item.next) to get all chained nodes

        old_storage = self.hash_table
        self.hash_table = [None] * new_capacity

        for i, el in enumerate(old_storage):
            if el is not None:
                self.put(el.key, el.value)

            curr_node = el

            if curr_node is not None:
                # add all chained nodes
                while curr_node.next is not None:
                    curr_node = curr_node.next
                    if curr_node is not None:
                        self.put(curr_node.key, curr_node.value)

                    
    # helper function to keep other methods more DRY
    def determine_resize_type(self):
        load_factor = self.get_load_factor()

        # double size of self.hash_table
        if load_factor > 0.7:
            self.resize(self.capacity * 2)

        # halve size of self.hash_table
        elif load_factor < 0.2:
            self.resize(self.capacity // 2)


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
