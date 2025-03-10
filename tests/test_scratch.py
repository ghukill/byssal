def test_repo_run_single_crawler(repository, local_fs_crawler):
    repository.run_crawlers(crawlers=[local_fs_crawler])
    with repository.get_connection() as conn:
        cur = conn.cursor()
        assert len(cur.execute("""select * from thread;""").fetchall()) == 5