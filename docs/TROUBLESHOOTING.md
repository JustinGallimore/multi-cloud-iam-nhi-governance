## Nested scripts folder caused "No such file or directory" error

**Symptom:**
Running `python scripts/attestation_report.py` returned:
`can't open file 'G:\HomeLab\Multi-Cloud-IAM-NHI-Governance\scripts\attestation_report.py': [Errno 2] No such file or directory`

**Root Cause:**
When the file was created, VS Code's file explorer was already expanded
into the scripts folder, causing the new file to be created one directory
level too deep at scripts/scripts/attestation_report.py instead of
scripts/attestation_report.py. The terminal was looking in the correct
top level scripts folder, but the file was not actually there.

**Fix:**
Confirmed the nesting by checking the breadcrumb path at the top of the
VS Code editor, which showed scripts > scripts > attestation_report.py.
Dragged the file up one level in the file explorer into the correct
scripts folder, deleted the now empty inner scripts folder, and reran
the script successfully.

**Lesson:**
Always check the breadcrumb path in the editor tab when a script reports
it cannot find a file that you know exists. A doubled folder name in the
breadcrumb is a fast way to catch a misplaced file before assuming the
code itself is broken.

## AWS Secret Access Key printed in terminal during aws configure

**Symptom:**
While rotating an AWS access key, running `aws configure` unexpectedly
printed the full Secret Access Key in plain text in the terminal
output, instead of masking it as expected.

**Root Cause:**
Terminal masking behavior for `aws configure` can vary depending on
terminal emulator and how input is echoed. In this case the secret
was visible in the terminal window at the moment a screenshot was
taken for documentation purposes.

**Fix:**
Treated the exposed key as compromised immediately, even though it had
not left the local machine in any other way. Deactivated and deleted
both the exposed key and the original key it was meant to replace,
then generated a third key and reconfigured the CLI without capturing
the configuration step in any screenshot.

**Lesson:**
Never screenshot the aws configure prompt itself. Only screenshot
verification commands like aws sts get-caller-identity, which confirm
the credentials work without ever displaying the secret. Any credential
that has been visible somewhere it should not have been, even briefly
and even locally, should be treated as compromised and rotated
immediately rather than assessed for actual risk.

## GitHub Actions workflow file missing from repo after commit

**Symptom:**
After committing and pushing Phase 6 work, the GitHub Actions tab
showed the "Get started with GitHub Actions" template gallery instead
of the OIDC Federation Test workflow. Navigating directly to
.github/workflows/oidc-test.yml on GitHub returned a 404, and the
commit history showed only 3 files changed, none of them the
workflow file, even though it existed locally and had shown up as
untracked in a previous git status check.

**Root Cause:**
The commit was made while the terminal's working directory was set
to terraform/aws, not the project root. git status always reports
the status of the entire repository regardless of the current
directory, so it correctly listed .github/workflows/oidc-test.yml as
untracked. However, git add . only stages files within the current
directory and its subdirectories. Running git add . from inside
terraform/aws staged only the three Terraform files sitting there
and silently excluded the workflow file at the project root, even
though git status had just shown it as pending.

**Fix:**
Navigated back to the project root, ran git status to reconfirm
oidc-test.yml was still untracked, then ran git add . from the root
so it correctly picked up the workflow file. Committed and pushed
again, this time bringing in the missing file along with several
screenshot additions that had also been sitting in the wrong scope.

**Lesson:**
git status and git add . can report and act on different scopes
depending on which directory the terminal is sitting in. git status
shows the whole repo, but git add . only stages the current folder
downward. Always run git add . from the project root, or explicitly
confirm what got staged with git status again immediately after
running git add, before committing.