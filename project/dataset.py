class DataSet():
    def __init__(self):
        self.datas = set()
    def collect_data(self, new_data):
        if new_data is None:
            return
        self.datas.update(new_data)

    def get_data(self):
        return self.datas

    def print_data(self):
        count = 1
        for data in self.datas:
            # output_file.write(data + '\n')
            print("%d : %s " % (count, data))
            count = count + 1


