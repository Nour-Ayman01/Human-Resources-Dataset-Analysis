
                                               --First: Creating Tables For Modelling--

CREATE TABLE Department (
    DepartmentID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentName VARCHAR(100)                          --1. Department Table--
);

INSERT INTO Department (DepartmentName)

SELECT DISTINCT Department
FROM HR_Analytics;



CREATE TABLE JobRole (
    JobRoleID INT IDENTITY(1,1) PRIMARY KEY,          --2. JobRole Table--
    JobRoleName VARCHAR(100),
    DepartmentID INT
);

INSERT INTO JobRole (
    JobRoleName,
    DepartmentID
)

SELECT DISTINCT
    HR_Analytics.JobRole,                 -- Linking Unique job roles with their department IDs--
    Department.DepartmentID

FROM HR_Analytics

JOIN Department
    ON HR_Analytics.Department = Department.DepartmentName;



    CREATE TABLE Employee (
    EmpID INT PRIMARY KEY,                    --3. Table Employee--
    Age INT,
    AgeGroup VARCHAR(50),
    Gender VARCHAR(20),
    MaritalStatus VARCHAR(50),
    Education INT,
    EducationField VARCHAR(100),
    DistanceFromHome INT
);

INSERT INTO Employee

SELECT DISTINCT
    EmpID,
    Age,
    AgeGroup,
    Gender,
    MaritalStatus,
    Education,
    EducationField,
    DistanceFromHome

FROM HR_Analytics;



CREATE TABLE Satisfaction (
    SatisfactionID INT IDENTITY(1,1) PRIMARY KEY,
    EnvironmentSatisfaction INT,
    JobSatisfaction INT,                                            -- Satisfaction Table--
    RelationshipSatisfaction INT,
    WorkLifeBalance INT
);

INSERT INTO Satisfaction (
    EnvironmentSatisfaction,
    JobSatisfaction,
    RelationshipSatisfaction,
    WorkLifeBalance
)

SELECT DISTINCT
    EnvironmentSatisfaction,
    JobSatisfaction,
    RelationshipSatisfaction,
    WorkLifeBalance

FROM HR_Analytics;



CREATE TABLE EmployeePerformance (                        --Fact Table( Employee Performance)
    PerformanceID INT IDENTITY(1,1) PRIMARY KEY,

    EmpID INT,
    JobRoleID INT,
    SatisfactionID INT,

    MonthlyIncome INT,
    DailyRate INT,
    HourlyRate INT,
    MonthlyRate INT,

    PercentSalaryHike INT,
    PerformanceRating INT,

    TotalWorkingYears INT,
    YearsAtCompany INT,
    YearsInCurrentRole INT,
    YearsSinceLastPromotion INT,
    YearsWithCurrManager INT,

    TrainingTimesLastYear INT,
    NumCompaniesWorked INT,

    Attrition VARCHAR(10),
    OverTime VARCHAR(10),

    Foreign Key (EmpID)                                           -- Creating EmployeePerformance As The Main Fact Table
    References Employee(EmpID),                                         -- Store Employee Performance, Salary, And Experience Data
    Foreign Key (JobRoleID)                                        -- Use Foreign Keys To Connect Employee, JobRole, And Satisfaction Tables
      References JobRole(JobRoleID),

    Foreign Key  (SatisfactionID)
        References Satisfaction(SatisfactionID)
);

ALTER TABLE EmployeePerformance

ADD CONSTRAINT FK_EmployeePerformance_Department

FOREIGN KEY (DepartmentID)
REFERENCES Department(DepartmentID);


INSERT INTO EmployeePerformance (

    EmpID,
    JobRoleID,
    SatisfactionID,

    MonthlyIncome,
    DailyRate,
    HourlyRate,
    MonthlyRate,

    PercentSalaryHike,
    PerformanceRating,

    TotalWorkingYears,
    YearsAtCompany,
    YearsInCurrentRole,
    YearsSinceLastPromotion,
    YearsWithCurrManager,

    TrainingTimesLastYear,
    NumCompaniesWorked,

    Attrition,
    OverTime
)

SELECT

    HR_Analytics.EmpID,
    JobRole.JobRoleID,
    Satisfaction.SatisfactionID,
    HR_Analytics.MonthlyIncome,
    HR_Analytics.PerformanceRating,
    HR_Analytics.Attrition

FROM HR_Analytics

JOIN JobRole
    ON HR_Analytics.JobRole = JobRole.JobRoleName

JOIN Satisfaction
    ON HR_Analytics.JobSatisfaction = Satisfaction.JobSatisfaction;



                                                    --Data Quality Check--
                                                                    -- Number Of Employees--
Select EmpID, COUNT(*) AS Duplicate_Count
From HR_Analytics
GROUP BY EmpID
HAVING COUNT(*) > 1;


Select  COUNT(*) AS Total_Employees             --Number Of Total Employees--
FROM HR_Analytics;

                                       --Distinct Departments With Employee Count--


                                                                         --Attrition Summuary--
Select Department, COUNT(*) AS Employee_Count
From HR_Analytics                                      --961 in Reasearch&Development,  446 in Sales , 63 in Human Resorces--
GROUP BY Department
ORDER BY Employee_Count DESC;

   -- -Analyze Attrition Count By Department

SELECT  Department,  COUNT(*) AS Attrition_Count
FROM HR_Analytics
WHERE Attrition = 1
GROUP BY Department                         -- Reasearch&Development department  Has the Highest Attrition--
ORDER BY Attrition_Count DESC;



Select JobRole, COUNT(*) AS Attrition_Count                        -- Analyze Attrition By Job Role
From HR_Analytics
WHERE Attrition = 1
GROUP BY JobRole
ORDER BY Attrition_Count DESC;



Select  JobSatisfaction, COUNT(*) AS Total_Employees,
SUM(Case When Attrition = '1' THEN 1 ELSE 0 END) AS Attrition_Count,
100.0 * SUM(Case When Attrition = '1' THEN 1 ELSE 0 END) / COUNT(*) AS Attrition_Picture_Rate          
From HR_Analytics

GROUP BY JobSatisfaction                         -- Analyze The Relationship Between Job Satisfaction And Employee Attrition Rate--
ORDER BY JobSatisfaction;


-- Analyze Attrition By Overtime

Select  OverTime,COUNT(*) AS Total_Employees,
Sum(CASE  WHEN Attrition = 1  THEN 1  ELSE 0 END) AS Attrition_Count
From HR_Analytics
GROUP BY OverTime                       --127 Attrition who work over time--
ORDER BY Attrition_Count DESC;


-- Analyze Attrition By Gender

Select Gender ,COUNT(*) AS Total_Employees,SUM(Case  WHEN Attrition = 1  THEN 1  ELSE 0 END) AS Attrition_Count
From HR_Analytics
GROUP BY Gender
ORDER BY Attrition_Count DESC;


                                                        --Salary Statistics--
 Select MIN(MonthlyIncome) AS Lowest_Salary,
  MAX(MonthlyIncome) AS Highest_Salary,
  AVG(MonthlyIncome) AS Average_Salary
FROM HR_Analytics;



                                                 -- Categoraize Monthly Income into Labels to show Highest Attrition Count--

Select Case When  MonthlyIncome < 3500 THEN 'Low Salary'
WHEN MonthlyIncome < 7000 THEN 'Medium Salary'
ELSE 'High Salary'
END AS Salary_Group,
COUNT(*) AS Attrition_Count
From HR_Analytics
Where Attrition = 1

GROUP BY
Case
    WHEN MonthlyIncome < 3500 THEN 'Low Salary'
    WHEN MonthlyIncome < 7000 THEN 'Medium Salary'
    ELSE 'High Salary'
END;



                                          -- Analyze Employee Distribution Across Age Groups--
Select AgeGroup, COUNT(*) AS Employee_Count
From HR_Analytics
GROUP BY AgeGroup
ORDER BY AgeGroup;



Select Case  WHEN HourlyRate < 40 THEN 'Low Hourly Rate'
 WHEN HourlyRate < 70 THEN 'Medium Hourly Rate' ELSE 'High Hourly Rate' END AS HourlyRate_Group,
COUNT(*) AS Attrition_Count
From HR_Analytics
WHERE Attrition = 1
GROUP BY CASE
  WHEN HourlyRate < 40 THEN 'Low Hourly Rate'
   WHEN HourlyRate < 70 THEN 'Medium Hourly Rate'  ELSE 'High Hourly Rate'    END;


                                                 

Select Case   WHEN DistanceFromHome <= 10 THEN 'Near' When DistanceFromHome <= 20 THEN 'Moderate'
ELSE 'Far'
       END AS Distance_Group,                                                     
                                                                              -- Analyzing Attrition By Distance From Home
COUNT(*) AS Attrition_Count
From HR_Analytics
WHERE Attrition = 1
GROUP BY Case
WHEN DistanceFromHome <= 10 THEN 'Near' WHEN DistanceFromHome <= 20 THEN 'Moderate'
 ELSE 'Far'
     END;

                                                               --Years Since Last Promotion VS Attrition--
Select YearsSinceLastPromotion,COUNT(*) AS Attrition_Count
From HR_Analytics
WHERE Attrition = 1
GROUP BY YearsSinceLastPromotion
ORDER BY YearsSinceLastPromotion;


                                                  -- Analyze Attrition By Job Level Categories--

Select Case WHEN JobLevel <= 2 THEN 'Entry Level'
WHEN JobLevel <= 4 THEN 'Mid Level'
 ELSE 'Senior Level'
 END AS JobLevel_Category,
COUNT(*) AS Attrition_Count
From HR_Analytics
WHERE Attrition = 1

GROUP BY Case
   WHEN JobLevel <= 2 THEN 'Entry Level'
  WHEN JobLevel <= 4 THEN 'Mid Level'
             ELSE 'Senior Level'
         END;


         -- Analyze Attrition By Environment Satisfaction
Select Case  WHEN EnvironmentSatisfaction = 1 THEN 'Low Satisfaction'
 WHEN EnvironmentSatisfaction = 2 THEN 'Medium Satisfaction'
 WHEN EnvironmentSatisfaction = 3 THEN 'High Satisfaction'
  ELSE 'Very High Satisfaction'
   END AS EnvironmentSatisfaction_Label,

COUNT(*) AS Attrition_Count
From HR_Analytics
WHERE Attrition = 1

GROUP BY Case WHEN EnvironmentSatisfaction = 1 THEN 'Low Satisfaction'
   WHEN EnvironmentSatisfaction = 2 THEN 'Medium Satisfaction'
   WHEN EnvironmentSatisfaction = 3 THEN 'High Satisfaction'
       ELSE 'Very High Satisfaction'
     END;
                                               
                                               --Business Travel & Attrition--
 Select BusinessTravel, COUNT(*) AS Attrition_Count      
From HR_Analytics
WHERE Attrition = 1
GROUP BY BusinessTravel
ORDER BY Attrition_Count DESC;


                                                

                                       --End--