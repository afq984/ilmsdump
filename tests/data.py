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

MATERIAL_2004666 = ilmsdump.Material(
    id=2004666,
    title='Syllabus',
    type='Econtent',
    course=COURSE_40596,
)

MATERIAL_258234 = ilmsdump.Material(
    id=258234,
    title='101學年度iLMS數位學習平台9/21應用課程錄影檔',
    type='Epowercam',
    course=COURSE_74,
)

HOMEWORK_198377 = ilmsdump.Homework(
    id=198377,
    title='Lab1: Platform Introduction & MPI',
    course=COURSE_40596,
)

HOMEWORK_200355 = ilmsdump.Homework(
    id=200355,
    title='Final Project',
    course=COURSE_40596,
)
