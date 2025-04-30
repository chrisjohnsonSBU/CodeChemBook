###############################################################################
#
# ChemSymbols - a function containing the unicode strings for special characters
# that are common in chemistry
#
###############################################################################

from codechembook.chemformula import ChemFormula

def _enclose(text, html_center):
    if type(text) == str and type(html_center) == str:
        return '<' + html_center + '>' + text + '</' + html_center + '>'
    else:
        raise NameError('Please provide a string argument')

def textsub(text):
    """
    Return a piece of text that has added HTML subscript tags.
    
    Required Args:
    text (string): text that should be subscripted
        
    Returns:
    (string): subscripted text with HTML tags
    """
    return _enclose(text, 'sub')

def textsup(text):
    """
    Return a piece of text that has added HTML superscript tags.
    
    Required Args:
    text (string): text that should be superscripted
        
    Returns:
    (string): superscripted text with HTML tags
    """
    return _enclose(text, 'sup')

def textit(text):
    """
    Return a piece of text that has added HTML italics tags.
    
    Required Args:
    text (string): text that should be italicized
        
    Returns:
    (string): italicized text with HTML tags
    """
    return _enclose(text, 'i')

def textbf(text):
    """
    Return a piece of text that has added HTML bold face tags.
    
    Required Args:
    text (string): text that should be bold faced
        
    Returns:
    (string): bold face text with HTML tags
    """
    return _enclose(text, 'b')

def quickHTMLFormula(formula, charge = 0, name = None, CAS = None):
    '''
    Outputs a properly formatted chemical formula for use in HTML contexts.

    Required Params:
    formula (string): An unformatted chemical formula, without charge.

    Optional Params:
    charge (int):  The charge of the compound. (default: 0)
    name (string): The name of the compound. (default: None)
    CAS (string):  The CAS number. (default: None)

    Returns:
    (string): An HTML-formatted chemical formula.
    '''
    return ChemFormula(formula, charge = charge, name = name, cas = CAS).html.replace("<span class='ChemFormula'>", "").replace("</span>", "")

def quickLatexFormula(formula, charge = 0, name = None, CAS = None):
    '''
    Outputs a properly formatted chemical formula for use in Latex contexts.

    Required Params:
    formula (string): An unformatted chemical formula, without charge.

    Optional Params:
    charge (int):  The charge of the compound. (default: 0)
    name (string): The name of the compound. (default: None)
    CAS (string):  The CAS number. (default: None)

    Returns:
    (string): A Latex-formatted chemical formula.
    '''
    return ChemFormula(formula, charge = charge, name = name, cas = CAS).latex

def quickUnicodeFormula(formula, charge = 0, name = None, CAS = None):
    '''
    Outputs a properly formatted chemical formula for use in unicode.

    Required Params:
    formula (string): An unformatted chemical formula, without charge.

    Optional Params:
    charge (int):  The charge of the compound. (default: 0)
    name (string): The name of the compound. (default: None)
    CAS (string):  The CAS number. (default: None)

    Returns:
    (string): A unicode chemical formula.
    '''
    return ChemFormula(formula, charge = charge, name = name, cas = CAS).unicode




