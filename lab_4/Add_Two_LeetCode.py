class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        values = []
        current = self
        while current:
            values.append(str(current.val))
            current = current.next
        return " -> ".join(values)

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
        # - Получение сумммы из двух листов.
        result = self.list_to_number(l1) + self.list_to_number(l2)
        
        # - Первый метод преобразования числа в список цифр
        # result_str = str(result)
        # digit_list = list(result_str)
    
        # - Второй метод преобразования числа в список цифр
        # digit_list = [char for char in str(result)]

        # - Третий метод преобразования числа в список цифр
        digit_list = list(map(str, str(result)))

        # - Reverse List
        digit_list.reverse()

        head = ListNode(int(digit_list[0]))
        current = head
        for d in digit_list[1:]:
                current.next = ListNode(int(d))
                current = current.next
        # - Возвращение результата.
        return head

if __name__ == "__main__":
    sl = Solution()

    # Создание первого списка: 2 -> 4 -> 3
    l1 = ListNode(2)
    l1.append_next(4)
    l1.append_next(3)

    # Создание второго списка: 5 -> 6 -> 4
    l2 = ListNode(5)
    l2.append_next(6)
    l2.append_next(4)

    result_number = sl.addTwoNumbers(l1, l2)
    print(result_number) # Ожидаемый вывод: 807