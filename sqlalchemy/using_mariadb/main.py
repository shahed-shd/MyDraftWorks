import logging

import db_connection as db_conn
import declarative_approach as decl
import sql_expression_approach as sql_expr


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(thread)6d - %(threadName)s - %(filename)10s - %(lineno)3d - %(levelname)5s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    import pdb; pdb.set_trace()

    decl.query_specific_columns()

    decl.dispose()
    db_conn.dispose()


if __name__ == '__main__':
    main()
