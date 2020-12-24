import yarl

import ilmsdump

COURSE_74 = ilmsdump.Course(
    id=74,
    serial='0001',
    name='iLMS平台線上客服專區',
    is_admin=False,
)

COURSE_399 = ilmsdump.Course(
    id=399,
    serial='09810CS140107',
    is_admin=False,
    name='資訊系統應用Computer Systems & Applications',
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

# Special homework
COURSE_38353 = ilmsdump.Course(
    id=38353,
    serial='10720FL300606',
    is_admin=False,
    name='中級日語二Intermediate Japanese II',
)

# With open homework
COURSE_43492 = ilmsdump.Course(
    id=43492,
    serial='10820CS542100',
    is_admin=False,
    name='雲端計算Cloud Computing',
)

# Not open
COURSE_43491 = ilmsdump.Course(
    id=43491,
    serial='10820CS540300',
    is_admin=False,
    name='高等程式語言Advanced Programming Languages',
)

# With open group homework
COURSE_5430 = ilmsdump.Course(
    id=5430,
    serial='09910TM200202',
    is_admin=False,
    name='管理學Management',
)

# has linked material
COURSE_35305 = ilmsdump.Course(
    id=35305,
    serial='10710CS542200',
    is_admin=False,
    name='平行程式Parallel Programming',
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

# linked material
MATERIAL_2705536 = ilmsdump.Material(
    id=2705536,
    title='PDF 版本投影片＆作業',
    type='Econtent',
    course=COURSE_35305,
)

VIDEO_1518 = ilmsdump.Video(
    id=1518,
    url=yarl.URL('https://lms.nthu.edu.tw/sysdata/74/74/doc/f08b98ab0aeddfd0/video/video_hd.mp4'),
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

# Open homework submission
HOMEWORK_220144 = ilmsdump.Homework(
    id=220144,
    title='Slides for paper presentation',
    course=COURSE_43492,
)

SUBMITTED_2474481 = ilmsdump.SubmittedHomework(
    id=2474481,
    title='105062321',
    by='\u9673\u5f18\u6b23',
    course=COURSE_43492,
)

ATTACHMENT_2406879 = ilmsdump.Attachment(
    id=2406879,
    title='105062321.pdf',
    parent=SUBMITTED_2474481,
)

# Open group homework submission
HOMEWORK_18264 = ilmsdump.Homework(
    id=18264,
    title='第五章(G1)',
    course=COURSE_5430,
)

SUBMITTED_59376 = ilmsdump.SubmittedHomework(
    id=59376,
    title='管理學報告ppt_ch5',
    by='第 1 組',
    course=COURSE_5430,
)

ATTACHMENT_49113 = ilmsdump.Attachment(
    id=49113,
    title='管理學報告.pptx',
    parent=SUBMITTED_59376,
)

# open submission
HOMEWORK_182409 = ilmsdump.Homework(
    id=182409,
    title='第一次作業 日語動詞 た形 (指定歌曲)',
    course=COURSE_38353,
)

# multiple div[@id="main"]
HOMEWORK_183084 = ilmsdump.Homework(
    id=183084,
    title='第2次作業  L21課\u3000「~と思う／～と言う」相關句型的日語歌曲或新聞',
    course=COURSE_38353,
)

GROUPLIST_40596 = ilmsdump.GroupList(
    course=COURSE_40596,
)

# empty <a> text
HOMEWORK_32460 = ilmsdump.Homework(
    id=32460,
    title='HW3_ch8,ch9',
    course=ilmsdump.Course(
        id=7636,
        serial='10010CS342301',
        is_admin=False,
        name='作業系統Operating Systems',
    ),
)

ATTACHMENT_133807 = ilmsdump.Attachment(
    id=133807,
    title='HW3.pdf',
    parent=HOMEWORK_32460,
)

# https://github.com/afq984/ilmsdump/issues/12
ATTACHMENT_3847 = ilmsdump.Attachment(
    id=3847,
    title='ch04.ppt',
    parent=None,
)
