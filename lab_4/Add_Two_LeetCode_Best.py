class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def append_next(self, val: int):
        current_node = self
        while current_node.next:
            current_node = current_node.next
        current_node.next = ListNode(val)


class Solution:
    def list_to_number(self, node: ListNode | None) -> int:
        digits = []
        while node:
            digits.append(node.val)
            node = node.next
        digits.reverse()
        return int("".join(map(str, digits))) if digits else 0

    def addTwoNumbers(self, l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
        result = self.list_to_number(l1) + self.list_to_number(l2)

        digit_list = list(map(int, str(result)))
        digit_list.reverse()

        head = ListNode(digit_list[0])
        current = head
        for d in digit_list[1:]:
            current.next = ListNode(d)
            current = current.next
        return head


def linked_list_to_list(node: ListNode | None) -> list[int]:
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


if __name__ == "__main__":
    sl = Solution()

    l1 = ListNode(2)
    l1.append_next(4)
    l1.append_next(3)

    l2 = ListNode(5)
    l2.append_next(6)
    l2.append_next(4)

    result_number = sl.addTwoNumbers(l1, l2)
    print(linked_list_to_list(result_number))  # [7, 0, 8]
