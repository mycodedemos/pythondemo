DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` varchar(32) NOT NULL DEFAULT '',
  `user_id` varchar(32) NOT NULL DEFAULT '' COMMENT '管理按用户id',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '任务名称',
  `total_work` int(11) NOT NULL DEFAULT '0' COMMENT '总任务数量',
  `begin_work` int(11) NOT NULL DEFAULT '0' COMMENT '开始的任务数',
  `daily_work` int(11) NOT NULL DEFAULT '0' COMMENT '每天完成的数量',
  `total_day` int(11) NOT NULL DEFAULT '0' COMMENT '每天完成的数量',
  `begin_day` date NOT NULL COMMENT '开始的时间',
  `end_day` date NOT NULL COMMENT '结束的时间',
  `done_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '完成状态、0：外开始、1：已完成、2：进行中',
  `status_message` varchar(256) DEFAULT '' COMMENT '任务状态信息',
  `remark` varchar(1024) DEFAULT '' COMMENT '备注',
  `is_done` tinyint(1) NOT NULL DEFAULT '0',
  `is_del` tinyint(1) NOT NULL DEFAULT '0',
  `create_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `task_daily`;
CREATE TABLE `task_daily` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `task_id` varchar(32) NOT NULL DEFAULT '' COMMENT '任务id',
  `todo_work` int(11) NOT NULL DEFAULT '0' COMMENT '需要完成的工作',
  `done_work` int(11) NOT NULL DEFAULT '0' COMMENT '完成的工作',
  `work_day` date NOT NULL COMMENT '工作天',
  `remark` varchar(1024) DEFAULT '',
  `done_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '完成状态、0：没做任务、1：已完成、2：超额完成、3：未完成',
  `is_del` tinyint(1) NOT NULL DEFAULT '0',
  `create_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;