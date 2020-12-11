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
