from utils.mongo_util import get_client, get_col

env = "test"

client = get_client(url='112.90.89.16', port=27017, username='myUserAdmin', password='8mwTdy1klnSYepNo')
db = "preprocessed"
search_dev_col = get_col(client, db, 'search.dev')
search_test_col = get_col(client, db, 'search.test')
zhidao_dev_col = get_col(client, db, 'zhidao.dev')
zhidao_test_col = get_col(client, db, 'zhidao.test')


