from __future__ import division

class Page:

    def __init__(self, number):
        self.number = number
        self.is_active = False

    def __repr__(self):
        if self.is_active:
            return "Page: {} (active)".format(self.number)
        else:
            return "Page: {}".format(self.number)


class Paginate:

    def __init__(self, count, current_page_number):
        self.current_page_number = max(current_page_number, 1)
        self.limit = 10
        self.offset = (current_page_number-1) * self.limit
        page_count = count / self.limit
        remainder = abs(page_count - round(page_count))
        if remainder > 0:
            page_count += 1
        self.count = page_count
        self._number_iterator = 1

    def __iter__(self):
        return self

    def next(self):
        if self._number_iterator > self.count:
            raise StopIteration
        else:
            number = self._number_iterator
            self._number_iterator += 1
            page = Page(number)
            page.is_active = (number == self.current_page_number)
            return page


if __name__ == "__main__":
    pages = Paginate(10, 3)
    for page in pages:
        print(page)
    print(pages.limit)
    print(pages.offset)
