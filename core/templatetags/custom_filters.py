from django import template

register = template.Library()

@register.filter
def get_progress_step(status):
    """
    Returns the step number (1-4) based on the status.
    1: Filed
    2: Examination / Formality
    3: Publication (Journal)
    4: Registered
    """
    
    # Stage 1: Filing
    if status in ['received', 'sent_to_vienna']:
        return 1
    
    # Stage 2: Examination & Objections
    elif status in ['formality_check_pass', 'formality_check_fail', 'marked_for_exam', 'objected', 'exam_report_issued', 'ready_for_show_cause']:
        return 2
    
    # Stage 3: Publication
    elif status in ['advertised']:
        return 3
    
    # Stage 4: Registration
    elif status in ['registered']:
        return 4
    
    # Edge Cases (Refused/Withdrawn) - Inko alag color denge template mein
    return 0