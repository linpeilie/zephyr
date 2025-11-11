.. _smf:

状态机框架 (State Machine Framework)
#####################################

.. highlight:: c

概述 (Overview)
================

状态机框架 (SMF) 是一个与应用程序无关的框架,它为开发人员提供了一种将状态机集成到其应用程序中的简便方法。可以通过启用 :kconfig:option:`CONFIG_SMF` 选项将该框架添加到任何项目中。(The State Machine Framework (SMF) is an application agnostic framework that provides an easy way for developers to integrate state machines into their application. The framework can be added to any project by enabling the :kconfig:option:`CONFIG_SMF` option.)

状态创建 (State Creation)
==========================

状态由三个函数表示,其中一个函数实现进入动作 (Entry actions),另一个函数实现运行动作 (Run actions),最后一个函数实现退出动作 (Exit actions)。进入和退出函数的原型如下:``void funct(void *obj)``,运行动作的原型是 ``enum smf_state_result funct(void *obj)``,其中 ``obj`` 参数是用户定义的结构,该结构将状态机上下文 :c:struct:`smf_ctx` 作为其第一个成员。例如::(A state is represented by three functions, where one function implements the Entry actions, another function implements the Run actions, and the last function implements the Exit actions. The prototype for the entry and exit functions are as follows: ``void funct(void *obj)``, and the prototype for the run action is ``enum smf_state_result funct(void *obj)`` where the ``obj`` parameter is a user defined structure that has the state machine context, :c:struct:`smf_ctx`, as its first member. For example::)

   struct user_object {
      struct smf_ctx ctx;
      /* All User Defined Data Follows */
   };

:c:struct:`smf_ctx` 成员必须是第一个,因为状态机框架的函数使用 :c:macro:`SMF_CTX` 宏将用户定义的对象转换为 :c:struct:`smf_ctx` 类型。(The :c:struct:`smf_ctx` member must be first because the state machine framework's functions casts the user defined object to the :c:struct:`smf_ctx` type with the :c:macro:`SMF_CTX` macro.)

例如,不要这样做 ``(struct smf_ctx *)&user_obj``,您可以使用 ``SMF_CTX(&user_obj)``。(For example instead of doing this ``(struct smf_ctx *)&user_obj``, you could use ``SMF_CTX(&user_obj)``.)

默认情况下,状态可以没有祖先状态,从而产生平面状态机。但是要启用分层状态机的创建,必须启用 :kconfig:option:`CONFIG_SMF_ANCESTOR_SUPPORT` 选项。(By default, a state can have no ancestor states, resulting in a flat state machine. But to enable the creation of a hierarchical state machine, the :kconfig:option:`CONFIG_SMF_ANCESTOR_SUPPORT` option must be enabled.)

运行动作的返回值 :c:enum:`smf_state_result` 决定状态机是否将事件传播到父运行动作 (:c:enum:`SMF_EVENT_PROPAGATE`) 或事件是否由运行动作处理 (:c:enum:`SMF_EVENT_HANDLED`)。平面状态机没有父动作,因此返回代码被忽略;建议返回 :c:enum:`SMF_EVENT_HANDLED`。(The return value of the run action, :c:enum:`smf_state_result` determines if the state machine propagates the event to parent run actions (:c:enum:`SMF_EVENT_PROPAGATE`) or if the event was handled by the run action (:c:enum:`SMF_EVENT_HANDLED`). Flat state machines do not have parent actions, so the return code is ignored; returning :c:enum:`SMF_EVENT_HANDLED` is recommended.)

调用 :c:func:`smf_set_state` 会阻止调用父运行动作,即使返回 :c:enum:`SMF_EVENT_PROPAGATE`。(Calling :c:func:`smf_set_state` prevents calling parent run actions, even if :c:enum:`SMF_EVENT_PROPAGATE` is returned.)

默认情况下,分层状态机不支持在进入超状态时初始转换到子状态。要启用它们,必须启用 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` 选项。(By default, the hierarchical state machines do not support initial transitions to child states on entering a superstate. To enable them the :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` option must be enabled.)

以下宏可用于轻松创建状态:(The following macro can be used for easy state creation:)

* :c:macro:`SMF_CREATE_STATE` 创建状态 (Create a state)

状态机创建 (State Machine Creation)
====================================

状态机是通过定义由枚举索引的状态表来创建的。例如,以下代码创建了三个平面状态::(A state machine is created by defining a table of states that's indexed by an enum. For example, the following creates three flat states::)

   enum demo_state { S0, S1, S2 };

   const struct smf_state demo_states[] = {
      [S0] = SMF_CREATE_STATE(s0_entry, s0_run, s0_exit, NULL, NULL),
      [S1] = SMF_CREATE_STATE(s1_entry, s1_run, s1_exit, NULL, NULL),
      [S2] = SMF_CREATE_STATE(s2_entry, s2_run, s2_exit, NULL, NULL)
   };

此示例创建了三个分层状态::(And this example creates three hierarchical states::)

   enum demo_state { S0, S1, S2 };

   const struct smf_state demo_states[] = {
      [S0] = SMF_CREATE_STATE(s0_entry, s0_run, s0_exit, parent_s0, NULL),
      [S1] = SMF_CREATE_STATE(s1_entry, s1_run, s1_exit, parent_s12, NULL),
      [S2] = SMF_CREATE_STATE(s2_entry, s2_run, s2_exit, parent_s12, NULL)
   };


此示例创建了三个分层状态,其中从父状态 S0 到子状态 S2 具有初始转换::(This example creates three hierarchical states with an initial transition from parent state S0 to child state S2::)

   enum demo_state { S0, S1, S2 };

   /* Forward declaration of state table */
   const struct smf_state demo_states[];

   const struct smf_state demo_states[] = {
      [S0] = SMF_CREATE_STATE(s0_entry, s0_run, s0_exit, NULL, demo_states[S2]),
      [S1] = SMF_CREATE_STATE(s1_entry, s1_run, s1_exit, demo_states[S0], NULL),
      [S2] = SMF_CREATE_STATE(s2_entry, s2_run, s2_exit, demo_states[S0], NULL)
   };

要设置初始状态,应调用 :c:func:`smf_set_initial` 函数。(To set the initial state, the :c:func:`smf_set_initial` function should be called.)

要从一个状态转换到另一个状态,使用 :c:func:`smf_set_state` 函数。(To transition from one state to another, the :c:func:`smf_set_state` function is used.)

.. note:: 如果未设置 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION`,则不应将父状态传递给 :c:func:`smf_set_initial` 和 :c:func:`smf_set_state` 函数,因为父状态不知道要转换到哪个子状态。如果定义了到子状态的初始转换,则转换到父状态是可以的。良好形成的 HSM 应该为所有父状态定义初始转换。(If :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` is not set, :c:func:`smf_set_initial` and :c:func:`smf_set_state` function should not be passed a parent state as the parent state does not know which child state to transition to. Transitioning to a parent state is OK if an initial transition to a child state is defined. A well-formed HSM should have initial transitions defined for all parent states.)

.. note:: 在状态机运行时,:c:func:`smf_set_state` 应仅从进入或运行函数调用。从退出函数调用 :c:func:`smf_set_state` 将在日志中生成警告,并且不会发生转换。(While the state machine is running, :c:func:`smf_set_state` should only be called from the Entry or Run function. Calling :c:func:`smf_set_state` from Exit functions will generate a warning in the log and no transition will occur.)

状态机执行 (State Machine Execution)
=====================================

要运行状态机,应以某种应用程序相关的方式调用 :c:func:`smf_run_state` 函数。如果它返回非零值,应用程序应停止调用 smf_run_state。(To run the state machine, the :c:func:`smf_run_state` function should be called in some application dependent way. An application should cease calling smf_run_state if it returns a non-zero value.)

状态机终止 (State Machine Termination)
=======================================

要终止状态机,应调用 :c:func:`smf_set_terminate` 函数。它可以从进入、运行或退出动作调用。该函数采用非零用户定义值,该值将由 :c:func:`smf_run_state` 函数返回。(To terminate the state machine, the :c:func:`smf_set_terminate` function should be called. It can be called from the entry, run, or exit actions. The function takes a non-zero user defined value that will be returned by the :c:func:`smf_run_state` function.)

检索当前状态 (Retrieving the Current State)
============================================

**叶状态** (Leaf State):在分层状态机的上下文中,*叶状态*是不包含任何子状态的状态。它表示层次结构中最细粒度的状态级别,在这里不可能进行进一步分解。(In the context of a hierarchical state machine, a *leaf state* is a state that does not contain any child states. It represents the most granular level of state in the hierarchy, where no further decomposition is possible.)

**执行状态** (Executing State):*执行状态*是指其进入、运行或退出动作当前正在由状态机执行的状态。这可以是父状态或叶状态,具体取决于当前操作。(The *executing state* refers to the state whose entry, run, or exit action is currently being executed by the state machine. This may be a parent or leaf state, depending on the current operation.)

要检索当前叶状态,应调用 :c:func:`smf_get_current_leaf_state` 函数。例如::(To retrieve the current leaf state, the :c:func:`smf_get_current_leaf_state` function should be called. For example::)

   const struct smf_state *leaf_state = smf_get_current_leaf_state(SMF_CTX(&s_obj));

.. note:: 如果未启用 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION`,或者如果未定义父状态的初始状态,则始终将状态设置为叶状态。否则,状态机可能直接进入父状态,:c:func:`smf_get_current_leaf_state` 可能返回父状态而不是叶状态。确保为所有父状态正确配置初始转换,以避免形成不良的分层状态机。(If :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` is not enabled, or if the initial state of a parent state is not defined, always set the state to a leaf state. Otherwise, the state machine may enter a parent state directly, and :c:func:`smf_get_current_leaf_state` may return a parent state instead of a leaf state. Ensure initial transitions are properly configured for all parent states to avoid malformed hierarchical state machines.)

要检索其进入、运行或退出动作当前正在执行的状态,使用 :c:func:`smf_get_current_executing_state` 函数。(To retrieve the state whose entry, run, or exit action is currently being executed, use the :c:func:`smf_get_current_executing_state` function.)

UML 状态机 (UML State Machines)
==================

SMF 遵循 UML 分层状态机转换规则,即最小公共祖先的进入和退出动作在转换时不执行,除非所述转换是到自身的转换。(SMF follows UML hierarchical state machine rules for transitions i.e., the entry and exit actions of the least common ancestor are not executed on transition, unless said transition is a transition to self.)

UML StateMachines 规范可以在以下 UML 规范的第 14 章中找到:https://www.omg.org/spec/UML/ (The UML Specification for StateMachines may be found in chapter 14 of the UML specification available here: https://www.omg.org/spec/UML/)

SMF 在以下方面偏离 UML 规则:(SMF breaks from UML rules in:)

1. 在源状态的上下文中执行与转换相关的动作,而不是在执行退出动作之后。(Executing the actions associated with the transition within the context of the source state, rather than after the exit actions are performed.)
2. 仅允许到自身的外部转换,而不允许到子状态的转换。从超状态到子状态的转换被视为本地转换。(Only allowing external transitions to self, not to sub-states. A transition from a superstate to a child state is treated as a local transition.)
3. 禁止在退出动作中使用 :c:func:`smf_set_state` 进行转换。(Prohibiting transitions using :c:func:`smf_set_state` in exit actions.)

SMF 也不提供除初始伪状态之外的任何伪状态。可以通过从 'terminate' 状态的进入动作调用 :c:func:`smf_set_terminate` 来建模终止伪状态。通过为每个区域调用 :c:func:`smf_run_state` 来建模正交区域。(SMF also does not provide any pseudostates except the Initial Pseudostate. Terminate pseudostates can be modelled by calling :c:func:`smf_set_terminate` from the entry action of a 'terminate' state. Orthogonal regions are modelled by calling :c:func:`smf_run_state` for each region.)

状态机示例 (State Machine Examples)
======================

平面状态机示例 (Flat State Machine Example)
**************************

此示例使用 SMF 将以下状态图转换为代码,其中初始状态为 S0。(This example turns the following state diagram into code using the SMF, where the initial state is S0.)

.. graphviz::
   :caption: 平面状态机图 (Flat state machine diagram)

   digraph smf_flat {
      node [style=rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];
      STATE_S2 [shape = box];

      init -> STATE_S0;
      STATE_S0 -> STATE_S1;
      STATE_S1 -> STATE_S2;
      STATE_S2 -> STATE_S0;
   }

代码::(Code::)(If :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` is not enabled, or if the initial state of a parent state is not defined, always set the state to a leaf state. Otherwise, the state machine may enter a parent state directly, and :c:func:`smf_get_current_leaf_state` may return a parent state instead of a leaf state. Ensure initial transitions are properly configured for all parent states to avoid malformed hierarchical state machines.)

要检索其进入、运行或退出动作当前正在执行的状态,使用 :c:func:`smf_get_current_executing_state` 函数。(To retrieve the state whose entry, run, or exit action is currently being executed, use the :c:func:`smf_get_current_executing_state` function.)

UML State Machines
==================

SMF follows UML hierarchical state machine rules for transitions i.e., the
entry and exit actions of the least common ancestor are not executed on
transition, unless said transition is a transition to self.

The UML Specification for StateMachines may be found in chapter 14 of the UML
specification available here: https://www.omg.org/spec/UML/

SMF breaks from UML rules in:

1. Executing the actions associated with the transition within the context
   of the source state, rather than after the exit actions are performed.
2. Only allowing external transitions to self, not to sub-states. A transition
   from a superstate to a child state is treated as a local transition.
3. Prohibiting transitions using :c:func:`smf_set_state` in exit actions.

SMF also does not provide any pseudostates except the Initial Pseudostate.
Terminate pseudostates can be modelled by calling  :c:func:`smf_set_terminate`
from the entry action of a 'terminate' state. Orthogonal regions are modelled
by calling :c:func:`smf_run_state` for each region.

State Machine Examples
======================

Flat State Machine Example
**************************

This example turns the following state diagram into code using the SMF, where
the initial state is S0.

.. graphviz::
   :caption: Flat state machine diagram

   digraph smf_flat {
      node [style=rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];
      STATE_S2 [shape = box];

      init -> STATE_S0;
      STATE_S0 -> STATE_S1;
      STATE_S1 -> STATE_S2;
      STATE_S2 -> STATE_S0;
   }

Code::

	#include <zephyr/smf.h>

	/* Forward declaration of state table */
	static const struct smf_state demo_states[];

	/* List of demo states */
	enum demo_state { S0, S1, S2 };

	/* User defined object */
	struct s_object {
		/* This must be first */
		struct smf_ctx ctx;

		/* Other state specific data add here */
	} s_obj;

	/* State S0 */
	static void s0_entry(void *o)
	{
		/* Do something */
	}
	static enum smf_state_result s0_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S1]);
		return SMF_EVENT_HANDLED;
	}
	static void s0_exit(void *o)
	{
		/* Do something */
	}

	/* State S1 */
	static enum smf_state_result s1_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S2]);
		return SMF_EVENT_HANDLED;
	}
	static void s1_exit(void *o)
	{
		/* Do something */
	}

	/* State S2 */
	static void s2_entry(void *o)
	{
		/* Do something */
	}
	static enum smf_state_result s2_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S0]);
		return SMF_EVENT_HANDLED;
	}

	/* Populate state table */
	static const struct smf_state demo_states[] = {
		[S0] = SMF_CREATE_STATE(s0_entry, s0_run, s0_exit, NULL, NULL),
		/* State S1 does not have an entry action */
		[S1] = SMF_CREATE_STATE(NULL, s1_run, s1_exit, NULL, NULL),
		/* State S2 does not have an exit action */
		[S2] = SMF_CREATE_STATE(s2_entry, s2_run, NULL, NULL, NULL),
	};

	int main(void)
	{
		int32_t ret;

		/* Set initial state */
		smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

		/* Run the state machine */
		while(1) {
			/* State machine terminates if a non-zero value is returned */
			ret = smf_run_state(SMF_CTX(&s_obj));
			if (ret) {
				/* handle return code and terminate state machine */
				break;
			}
			k_msleep(1000);
		}
	}

Hierarchical State Machine Example
**********************************

This example turns the following state diagram into code using the SMF, where
S0 and S1 share a parent state and S0 is the initial state.


.. graphviz::
   :caption: Hierarchical state machine diagram

   digraph smf_hierarchical {
      node [style = rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];
      STATE_S2 [shape = box];

      subgraph cluster_0 {
         label = "PARENT";
         style = rounded;
         STATE_S0 -> STATE_S1;
      }

      init -> STATE_S0;
      STATE_S1 -> STATE_S2;
      STATE_S2 -> STATE_S0;
   }

Code::

	#include <zephyr/smf.h>

	/* Forward declaration of state table */
	static const struct smf_state demo_states[];

	/* List of demo states */
	enum demo_state { PARENT, S0, S1, S2 };

	/* User defined object */
	struct s_object {
		/* This must be first */
		struct smf_ctx ctx;

		/* Other state specific data add here */
	} s_obj;

	/* Parent State */
	static void parent_entry(void *o)
	{
		/* Do something */
	}
	static void parent_exit(void *o)
	{
		/* Do something */
	}

	/* State S0 */
	static enum smf_state_result s0_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S1]);
		return SMF_EVENT_HANDLED;
	}

	/* State S1 */
	static enum smf_state_result s1_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S2]);
		return SMF_EVENT_HANDLED;
	}

	/* State S2 */
	static enum smf_state_result s2_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S0]);
		return SMF_EVENT_HANDLED;
	}

	/* Populate state table */
	static const struct smf_state demo_states[] = {
		/* Parent state does not have a run action */
		[PARENT] = SMF_CREATE_STATE(parent_entry, NULL, parent_exit, NULL, NULL),
		/* Child states do not have entry or exit actions */
		[S0] = SMF_CREATE_STATE(NULL, s0_run, NULL, &demo_states[PARENT], NULL),
		[S1] = SMF_CREATE_STATE(NULL, s1_run, NULL, &demo_states[PARENT], NULL),
		/* State S2 do not have entry or exit actions and no parent */
		[S2] = SMF_CREATE_STATE(NULL, s2_run, NULL, NULL, NULL),
	};

	int main(void)
	{
		int32_t ret;

		/* Set initial state */
		smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

		/* Run the state machine */
		while(1) {
			/* State machine terminates if a non-zero value is returned */
			ret = smf_run_state(SMF_CTX(&s_obj));
			if (ret) {
				/* handle return code and terminate state machine */
				break;
			}
			k_msleep(1000);
		}
	}

When designing hierarchical state machines, the following should be considered:
 - Ancestor entry actions are executed before the sibling entry actions. For
   example, the parent_entry function is called before the s0_entry function.
 - Transitioning from one sibling to another with a shared ancestry does not
   re-execute the ancestor\'s entry action or execute the exit action.
   For example, the parent_entry function is not called when transitioning
   from S0 to S1, nor is the parent_exit function called.
 - Ancestor exit actions are executed after the exit action of the current
   state. For example, the s1_exit function is called before the parent_exit
   function is called.
 - The parent_run function only executes if the child_run function does not
   call either :c:func:`smf_set_state` or return :c:enum:`SMF_EVENT_HANDLED`.
 - Avoid malformed hierarchical state machines by ensuring the state always
   transitions to a leaf state when :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION`
   is not enabled, or when a parent state's initial state is undefined.

Event Driven State Machine Example
**********************************

Events are not explicitly part of the State Machine Framework but an event driven
state machine can be implemented using Zephyr :ref:`events`.

.. graphviz::
   :caption: Event driven state machine diagram

   digraph smf_flat {
      node [style=rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];

      init -> STATE_S0;
      STATE_S0 -> STATE_S1 [label = "BTN EVENT"];
      STATE_S1 -> STATE_S0 [label = "BTN EVENT"];
   }

Code::

	#include <zephyr/kernel.h>
	#include <zephyr/drivers/gpio.h>
	#include <zephyr/smf.h>

	#define SW0_NODE        DT_ALIAS(sw0)

	/* List of events */
	#define EVENT_BTN_PRESS BIT(0)

	static const struct gpio_dt_spec button =
		GPIO_DT_SPEC_GET_OR(SW0_NODE, gpios, {0});

	static struct gpio_callback button_cb_data;

	/* Forward declaration of state table */
	static const struct smf_state demo_states[];

	/* List of demo states */
	enum demo_state { S0, S1 };

	/* User defined object */
	struct s_object {
		/* This must be first */
		struct smf_ctx ctx;

		/* Events */
		struct k_event smf_event;
		int32_t events;

		/* Other state specific data add here */
	} s_obj;

	/* State S0 */
	static void s0_entry(void *o)
	{
		printk("STATE0\n");
	}

	static void s0_run(void *o)
	{
		struct s_object *s = (struct s_object *)o;

		/* Change states on Button Press Event */
		if (s->events & EVENT_BTN_PRESS) {
			smf_set_state(SMF_CTX(&s_obj), &demo_states[S1]);
		}
		return SMF_EVENT_HANDLED;
	}

	/* State S1 */
	static void s1_entry(void *o)
	{
		printk("STATE1\n");
	}

	static void s1_run(void *o)
	{
		struct s_object *s = (struct s_object *)o;

		/* Change states on Button Press Event */
		if (s->events & EVENT_BTN_PRESS) {
			smf_set_state(SMF_CTX(&s_obj), &demo_states[S0]);
		}
		return SMF_EVENT_HANDLED;
	}

	/* Populate state table */
	static const struct smf_state demo_states[] = {
		[S0] = SMF_CREATE_STATE(s0_entry, s0_run, NULL, NULL, NULL),
		[S1] = SMF_CREATE_STATE(s1_entry, s1_run, NULL, NULL, NULL),
	};

	void button_pressed(const struct device *dev,
			struct gpio_callback *cb, uint32_t pins)
	{
		/* Generate Button Press Event */
		k_event_post(&s_obj.smf_event, EVENT_BTN_PRESS);
	}

	int main(void)
	{
		int ret;

		if (!gpio_is_ready_dt(&button)) {
			printk("Error: button device %s is not ready\n",
				button.port->name);
			return;
		}

		ret = gpio_pin_configure_dt(&button, GPIO_INPUT);
		if (ret != 0) {
			printk("Error %d: failed to configure %s pin %d\n",
				ret, button.port->name, button.pin);
			return;
		}

		ret = gpio_pin_interrupt_configure_dt(&button,
			GPIO_INT_EDGE_TO_ACTIVE);
		if (ret != 0) {
			printk("Error %d: failed to configure interrupt on %s pin %d\n",
				ret, button.port->name, button.pin);
			return;
		}

		gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));
		gpio_add_callback(button.port, &button_cb_data);

		/* Initialize the event */
		k_event_init(&s_obj.smf_event);

		/* Set initial state */
		smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

		/* Run the state machine */
		while(1) {
			/* Block until an event is detected */
			s_obj.events = k_event_wait(&s_obj.smf_event,
					EVENT_BTN_PRESS, true, K_FOREVER);

			/* State machine terminates if a non-zero value is returned */
			ret = smf_run_state(SMF_CTX(&s_obj));
			if (ret) {
				/* handle return code and terminate state machine */
				break;
			}
		}
	}

State Machine Example With Initial Transitions And Transition To Self
*********************************************************************

:zephyr_file:`tests/lib/smf/src/test_lib_self_transition_smf.c` defines a state
machine for testing the initial transitions and transitions to self in a parent
state. The statechart for this test is below.


.. graphviz::
   :caption: Test state machine for UML State Transitions

   digraph smf_hierarchical_initial {
      compound=true;
      node [style = rounded];
      "smf_set_initial()" [shape=plaintext fontname=Courier];
      ab_init_state [shape = point];
      STATE_A [shape = box];
      STATE_B [shape = box];
      STATE_C [shape = box];
      STATE_D [shape = box];
      DC[shape=point height=0 width=0 label="" style="invis"]

      subgraph cluster_root {
         label = "ROOT";
         style = rounded;

         subgraph cluster_ab {
            label = "PARENT_AB";
            style = rounded;
            ab_init_state -> STATE_A;
            STATE_A -> STATE_B;
         }

         subgraph cluster_c {
            label = "PARENT_C";
            style = rounded;
            STATE_B -> STATE_C [ltail=cluster_ab]
         }

         STATE_C -> DC [ltail=cluster_c, dir=none];
         DC -> STATE_C [lhead=cluster_c];
         STATE_C -> STATE_D
      }

      "smf_set_initial()" -> STATE_A [lhead=cluster_ab]
   }


API Reference
=============

.. doxygengroup:: smf
