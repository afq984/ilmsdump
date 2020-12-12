import yarl

import ilmsdump


COURSE_74 = ilmsdump.Course(
    id=74,
    serial='0001',
    name='iLMS平台線上客服專區',
    is_admin=False,
)

COURSE_46274 = ilmsdump.Course(
    id=46274,
    serial='10910CS542200',
    name='平行程式Parallel Programming',
    is_admin=False,
)

COURSE_40596 = ilmsdump.Course(
    id=40596,
    serial='10810CS542200',
    name='平行程式Parallel Programming',
    is_admin=False,
)

# has only material
COURSE_1808 = ilmsdump.Course(
    id=1808,
    serial='09810BMES525100',
    name='藥物控制釋放Drug Controlled Release',
    is_admin=False,
)

# has only discussion
COURSE_359 = ilmsdump.Course(
    id=359,
    serial='09810CL492400',
    name='敦煌學Dunhuang Studies',
    is_admin=False,
)

ANNOUNCEMENT_2218728 = ilmsdump.Announcement(
    id=2218728,
    title='HW3 成績公佈',
    course=COURSE_40596,
)

ATTACHMENT_2616319 = ilmsdump.Attachment(
    id=2616319,
    title='announcement.txt',
    parent=ANNOUNCEMENT_2218728,
)

ATTACHMENT_2616320 = ilmsdump.Attachment(
    id=2616320,
    title='announcement_updated.txt',
    parent=ANNOUNCEMENT_2218728,
)

ATTACHMENT_2616322 = ilmsdump.Attachment(
    id=2616322,
    title='meta.json',  # shall be renamed to meta_.json when saved
    parent=ANNOUNCEMENT_2218728,
)

ANNOUNCEMENT_2008652 = ilmsdump.Announcement(
    id=2008652,
    title='Final Project 分組',
    course=COURSE_40596,
)

DISCUSSION_258543 = ilmsdump.Discussion(
    id=258543,
    title='不能 srun - QOSMaxGRESMinutesPerJob',
    course=COURSE_40596,
)

ATTACHMENT_2134734 = ilmsdump.Attachment(
    id=2134734,
    title='hw4-2-QOSMaxGRESMinutesPerJob-srun.png',
    parent=DISCUSSION_258543,
)

ATTACHMENT_2134738 = ilmsdump.Attachment(
    id=2134738,
    title='hw4-2-QOSMaxGRESMinutesPerJob.png',
    parent=DISCUSSION_258543,
)

DISCUSSION_236608 = ilmsdump.Discussion(
    id=236608,
    title='誠徵final project組員',
    course=COURSE_40596,
)

MATERIAL_2173495 = ilmsdump.Material(
    id=2173495,
    title='Chap12: Distributed Computing for DL',
    type='Econtent',
    course=COURSE_40596,
)

ATTACHMENT_2107249 = ilmsdump.Attachment(
    id=2107249,
    title='Chap12_Distributed Computing for DL.pdf',
    parent=MATERIAL_2173495,
)

MATERIAL_2004666 = ilmsdump.Material(
    id=2004666,
    title='Syllabus',
    type='Econtent',
    course=COURSE_40596,
)

MATERIAL_1518 = ilmsdump.Material(
    id=1518,
    title='PowerCam5 簡報錄影軟體',
    type='Epowercam',
    course=COURSE_74,
)

VIDEO_1518 = ilmsdump.Video(
    id=1518,
    url=yarl.URL('http://lms.nthu.edu.tw/sysdata/74/74/doc/f08b98ab0aeddfd0/video/video_hd.mp4'),
)

HOMEWORK_198377 = ilmsdump.Homework(
    id=198377,
    title='Lab1: Platform Introduction & MPI',
    course=COURSE_40596,
)

HOMEWORK_201015 = ilmsdump.Homework(
    id=201015,
    title='HW3: All-Pairs Shortest Path (CPU)',
    course=COURSE_40596,
)

ATTACHMENT_2038513 = ilmsdump.Attachment(
    id=2038513,
    title='PP2019_HW3.pdf',
    parent=HOMEWORK_201015,
)

ATTACHMENT_2047732 = ilmsdump.Attachment(
    id=2047732,
    title='PP2019_HW3_v2.pdf',
    parent=HOMEWORK_201015,
)

HOMEWORK_200355 = ilmsdump.Homework(
    id=200355,
    title='Final Project',
    course=COURSE_40596,
)
