.. _on_demand_policy:

按需CPU频率调节策略 (On-Demand CPU Frequency Scaling Policy)
#############################################################

按需策略使用 :ref:`CPU负载指标 <cpu_load_metric>` 评估当前CPU负载,并将其与SoC P-state定义中定义的触发阈值进行比较 (The On-Demand policy evaluates the current CPU load using the :ref:`CPU Load metric <cpu_load_metric>`, and compares it to the trigger threshold defined by the SoC P-state definition)。

按需策略将遍历已定义的P-state,并选择CPU负载超过定义阈值的第一个P-state (The On-Demand policy will iterate through the defined P-states and select the first P-state of which the CPU load exceeds the defined threshold)。

有关按需策略的示例,请参阅 :zephyr:code-sample:`cpu_freq_on_demand` 示例 (For an example of the on-demand policy refer to the :zephyr:code-sample:`cpu_freq_on_demand` sample)。

此策略是反应式的 (This policy is reactive)。频率调整仅在观察到系统负载变化后发生,因此无法预测突然的高负载 (Frequency adjustments occur only after a change in system load has been observed, so it cannot anticipate sudden high loads)。该策略没有任务截止时间的概念,不应被视为实时策略 (The policy has no notion of task deadlines and should not be considered as a real-time policy)。
