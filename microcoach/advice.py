def generate_advice(user_stats, pro_stats):
    tips = []
    if user_stats.get("step_len",0) > pro_stats.get("step_len",1)*1.25:
        tips.append("Shorten your step length; add extra micro-clicks when dodging.")
    if user_stats.get("dir_change_rate",0) < pro_stats.get("dir_change_rate",1)*0.8:
        tips.append("Increase direction changes per second during trades.")
    if user_stats.get("curvature",0) < pro_stats.get("curvature",1)*0.8:
        tips.append("Your path is too straight; add slight arcs to avoid linear skillshots.")
    if user_stats.get("jitter",0) > pro_stats.get("jitter",1)*1.2:
        tips.append("Smooth out over-corrections; reduce jitter between clicks.")
    return tips or ["Solid fundamentals—practice orbwalk timing next."]
