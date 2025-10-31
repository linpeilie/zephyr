.. _modifying_contributions:

修改其他开发者的贡献 (Modifying Contributions made by other developers)
********************************************************************

场景 (Scenarios)
################

我们鼓励 Zephyr 的贡献者与协作者在 Pull Request 中作为评审者参与，这样补丁可作为原始 PR 的一部分被批准并合入 Zephyr 的主分支。PR 的作者负责在评审流程中修订 (amend) 其最初的提交。

然而在某些情况下，贡献者可能需要修改由其他 Zephyr 贡献者提交到 PR 中的补丁。例如：

* 开发者将其他贡献者提交的 commit 拣选 (cherry-pick) 到自己的 PR 中，以便：

  * 合入某个已“滞留 (stale)”PR 中的有用内容，或
  * 将其作为更大补丁的一部分一并合入主分支

* 开发者向其他贡献者创建的分支或 PR 进行推送，以便：

  * 协助更新 PR，从而将补丁合入主分支

  * 推动滞留 PR 完成并最终合并


可接受的策略 (Accepted policies)
################################

打算拣选、并可能修改其他贡献者提交的补丁时，开发者应：

* 在自己的 PR 中说明为何选择拣选这些补丁，而非协助在其原始 PR 中完成合入；并且
* 邀请补丁的原作者参与自己 PR 的评审。

打算向其他 Zephyr 贡献者的分支或 PR 进行强制推送 (force-push) 时，开发者应在 PR 中说明推送与修改已有补丁的原因（例如：当 PR 作者无法处理时，这是为了推动该 PR 评审完成）。

.. note::
  开发者应尽量将上述做法限制在被识别为 *stale* 的 PR 上。如何识别滞留 PR，见 :ref:`development processes and tools <dev-environment-and-tools>`。

如果对原始补丁进行了实质性修改，开发者可以：

* （更推荐）联系原作者，请其确认在保留原作者的 Signed-off-by 行与作者信息的情况下，允许合并修改后的补丁；或
* 将修改后的补丁作为自己的工作提交（即使用 *自己的* Signed-off-by 行与作者身份）。此时，开发者应在提交信息中标明该工作基于的“原始来源”（例如提及原 PR 编号）。

.. note::
  若你不希望其他 Zephyr 开发者在你原始分支或 PR 中修改补丁，请取消勾选 *“Allow Edits By Maintainers”* 选项。
.. _modifying_contributions:

Modifying Contributions made by other developers
************************************************

Scenarios
#########

Zephyr contributors and collaborators are encouraged to assist
as reviewers in pull requests, so that patches may be approved and merged
to Zephyr's main branch as part of the original pull requests. The authors
of the pull requests are responsible for amending their original commits
following the review process.

There are occasions, however, when a contributor might need to modify patches
included in pull requests that are submitted by other Zephyr contributors.
For instance, this is the case when:

* a developer cherry-picks commits submitted by other contributors into their
  own pull requests in order to:

  * integrate useful content which is part of a stale pull request, or
  * get content merged to the project's main branch as part of a larger
    patch

* a developer pushes to a branch or pull request opened by another
  contributor in order to:

  * assist in updating pull requests in order to get the patches merged
    to the project's main branch
  * drive stale pull requests to completion so they can be merged


Accepted policies
#################

A developer who intends to cherry-pick and potentially modify patches sent by
another contributor shall:

* clarify in their pull request the reason for cherry-picking the patches,
  instead of assisting in getting the patches merged in their original
  pull request, and
* invite the original author of the patches to their pull request review.

A developer who intends to force-push to a branch or pull request of
another Zephyr contributor shall clarify in the pull request the reason
for pushing and for modifying the existing patches (e.g. stating that it
is done to drive the pull request review to completion, when the pull
request author is not able to do so).

.. note::
  Developers should try to limit the above practice to pull requests identified
  as *stale*. Read about how to identify pull requests as stale in
  :ref:`development processes and tools <dev-environment-and-tools>`

If the original patches are substantially modified, the developer can either:

* (preferably) reach out to the original author and request them to
  acknowledge that the modified patches may be merged while having
  the original sign-off line and author identity, or
* submit the modified patches as their *own* work (i.e. with their
  *own* sign-off line and author identity). In this case, the developer
  shall identify in the commit message(s) the original source the
  submitted work is based on (mentioning, for example, the original PR
  number).

.. note::
  Contributors should uncheck the box *“Allow Edits By Maintainers"*
  to indicate that they do not wish their patches to be amended,
  inside their original branch or pull request, by other Zephyr developers.
