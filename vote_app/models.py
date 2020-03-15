from django.db import models

# Create your models here.

"""

用户表
	no 编号
	username 用户名
	password 密码


活动Activity
	no 编号
	title 标题
	picture 图片
	content 活动介绍
	rule 投票规则
	start_time 活动开始时间
	end_time 活动结束时间
	active 活动是否结束


活动类型ActivityType
	no 编号
	name 活动类型


活动详情ActivityDetail
	no 编号
	name 名称
	count 投票数

	activity_id 活动id 外键
	type_id 活动类型id 外键

投票记录VoteRecord
	no 编号
	activitydetail_id  活动详情id 外键 联合唯一外键
	user_id 用户id 外键 联合唯一外键
	vote_time 投票时间




投票首页
	/vote/home/1.html

投票主页面
	/vote/index/1.html

投一票接口
	post: /vote/voting
	data: {
		'activitydetail_id': 1,
		'user_id': 2
	}
"""

class UserInfo(models.Model):
    username = models.CharField(verbose_name="User Name", max_length=64, null=False, blank=False)
    password = models.CharField(verbose_name="PassWord", max_length=64, null=False, blank=False)


class Activity(models.Model):
    """活动表"""
    title = models.CharField(verbose_name="Activity Title", max_length=64,)
    img = models.ImageField(upload_to="media/upload/activity_img/", null=True, blank=True, verbose_name="Activity Image")
    content = models.TextField(verbose_name="Activity Content", null=True, blank=True)
    rule = models.TextField(verbose_name="Activity Rule", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="Activity Start Time", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="Activity End Time", null=True, blank=True)
    active = models.BooleanField(verbose_name="Activity Active", default=True)

    def __str__(self):
        return 'id: {self.id}, {self.title}'.format(self=self)


class ActivityDetail(models.Model):
    """活动细节表"""
    name = models.CharField(verbose_name="Activitu Detail Name", max_length=64, null=False, blank=False)
    vote_count = models.IntegerField("Activitu Detail Vote Count", default=0)
    thumb = models.ImageField(upload_to="media/upload/activity_detail_thumb/", null=True, blank=True, verbose_name="Activity Detail Thumbnail")
    file = models.FileField(upload_to="media/upload/activity_detail_file/", null=True, blank=True, verbose_name="Activity Detail File")
    content = models.TextField(verbose_name="Activity Detail Content", null=True, blank=True)
    activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name="Relation Activity")
    activity_type_id = models.CharField(verbose_name="Activity Page Type", max_length=64, choices=[
        ("video", "影音类"),
        ("picture", "图片类"),
        ("document", "文档类"),
    ], null=False, blank=False)

    def __str__(self):
        return 'id: {self.id}, {self.name}, {self.activity_type_id}'.format(self=self)


class VoteRecord(models.Model):
    """投票记录表"""
    activity_detail_id = models.ForeignKey(ActivityDetail, on_delete=models.CASCADE)
    activity_type = models.CharField(verbose_name="Activity Page Type", max_length=64)
    IP = models.CharField(verbose_name="IP", null=False, blank=False, max_length=64)
    vote_time = models.DateTimeField(verbose_name="Vote Record Create Time", auto_now_add=True)

    def __str__(self):
        return '{self.id}, {self.IP}, {self.activity_detail_id}'.format(self=self)

    class Meta:
        # 联合约束 其中 activity_detail_id 和 IP 不能重复
        unique_together = ["activity_detail_id", "IP"]




