-- 查看重复md5值得数据
select md5,count(0) as count from image where is_del = 0  group by md5 order by count desc;

-- 删除无效图片
delete from image where md5 = '2923b250a3660c034aa7831d5e6d7f3c';