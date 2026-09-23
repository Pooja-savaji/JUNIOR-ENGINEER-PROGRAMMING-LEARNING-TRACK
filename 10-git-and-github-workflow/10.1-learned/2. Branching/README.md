# 13.2 Branching

## Task
Practice Git branching by completing three independent tasks using separate feature branches.

## Branches Used
* `feature-student-info` - Added student information
* `feature-skills` - Added student skills
* `feature-contact` - Added contact information

## Work Completed

### 1. Student Information
Added:
* Name
* Course

### 2. Student Skills
Added:
* Python
* SQL
* Git

### 3. Contact Information
Added:
* Email

## Git Commands Practiced
git switch -c feature-student-info
git add student.txt
git commit -m "Add student info"

git switch master
git merge feature-student-info

git switch -c feature-skills
git add student.txt
git commit -m "Add student skills"

git switch master
git merge feature-skills

git switch -c feature-contact
git add student.txt
git commit -m "Add contact info"

git switch master
git merge feature-contact


## Result
* Created three independent feature branches.
* Made small commits on each branch.
* Merged all branches into `master`.
* Checked the Git history.
* Final working tree was clean.

## Learning
I learned how to create, use, switch, and merge Git branches while keeping commits small and organized.
