
# pylint: disable=I0011, C0111, C0302, too-few-public-methods, no-self-use, too-many-public-methods, invalid-name, unused-argument

from parsimonious_ext.expression_nodes import ALTERNATION, OPTIONAL, LITERAL, REGEX

from parsimonious.nodes import NodeVisitor

def camxes_node(node, visited_children, name=None):
    node_name = name or node.expr_name
    children = _children(node, visited_children)
    return _camxes_node(node_name, children)

def _camxes_node(name, children):
    if _is_nonempty_list(children) and _has_name_head(children):
        ret = [children] if name == None else [name, children]
    else:
        ret = _node_int(name, children)
    return ret

def _is_nonempty_list(obj):
    return isinstance(obj, list) and obj

def _has_name_head(seq):
    return isinstance(seq[0], basestring) and seq[0] != ""

def _node_int(name, args):
    if isinstance(args, basestring):
        ret = args
    else:
        ret = [] if name == None else [name]
        if args:
            _node_int_append_args(ret, args)
    return ret

def _node_int_append_args(ret, args):
    for arg in args:
        if arg and len(arg) != 0:
            ret.append(_node_int(None, arg))

def node_nonempty(node, visited_children, name=None):
    node_name = name or node.expr_name
    cam_node = camxes_node(node, visited_children, name)
    if len(cam_node) == 1 and cam_node[0] == node_name:
        return []
    else:
        return cam_node

def node_elidible(node, visited_children, name=None):
    node_name = name or node.expr_name
    node_name = node_name.replace("_elidible", "")
    children = _children(node, visited_children)
    if children == "":
        return [node_name]
    else:
        return _camxes_node(node_name, children)

def node2(node, visited_children, name=None):
    node_name = name or node.expr_name
    children = _children(node, visited_children)
    return _node2(node_name, children[0], children[1])

def _node2(node_name, child1, child2):
    return [node_name] + list(_camxes_node(child1, None)) + list(_camxes_node(child2, None))

def node_simple(node, visited_children, name=None):
    node_name = name or node.expr_name
    children = _children(node, visited_children)
    return _node_simple(node_name, children)

def _node_simple(node_name, children):
    return [node_name, children]

def _node_name(node):
    return node.expr_name

def node_simple_alias(node, visited_children, name=None):
    node_name = name or node.expr_name
    child = _look_past(visited_children)
    return [node_name, child]

def indexed(node, visited_children, i):
    children = _children(node, visited_children)
    return children[i]

def join_named(node, visited_children, name=None):
    node_name = name or node.expr_name
    children = _children(node, visited_children)
    return _join_named(node_name, children)

def _join_named(node_name, children):
    return [node_name, _join(children)]

def join_indexed(node, visited_children, i):
    children = _children(node, visited_children)
    return [node.expr_name, _join(children[i])]

def join_indexed_children(node, visited_children, i):
    children = _children(node, visited_children)
    return _join(children[i])

def join(node, visited_children):
    children = _children(node, visited_children)
    return _join(children)

def _join(children):
    if isinstance(children, basestring):
        return children
    else:
        ret = ""
        if children != None:
            for child in children:
                ret += _join(child)
        return ret

def default(node, visited_children):
    node_type = node.node_type()
    if node_type == LITERAL or node_type == REGEX:
        return node.text
    else:
        children = _children(node, visited_children)
        return children

# There are several differences in the parse tree produced by parsimonious,
# as compared to that produced by camxes.js:

# * alternation (/) expressions yield nodes, with the selected option as child
#
# * optional (?) expressions always yield nodes with the matched value as child,
#   or with "" as child if no value is matched

def _children(node, visited_children):
    node_type = node.node_type()
    if node_type == ALTERNATION:
        return _lift_child(visited_children)
    elif node_type == OPTIONAL:
        child = _lift_child(visited_children)
        return child or ""
    else:
        return visited_children

def _lift_child(children):
    child = None
    if isinstance(children, list):
        if len(children) == 1:
            child = children[0]
    return child

def _look_past(children):
    child = None
    if isinstance(children, list):
        if len(children) > 1:
            child = children[1]
    return child

def terminal(value):
    return value

class Transformer(object):

    def transform(self, parsed):
        return Visitor().visit(parsed)

class Visitor(NodeVisitor):

    # ___ GRAMMAR ___

    def visit_text(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_intro_null(self, node, visited_children):
        return node_nonempty(node, visited_children)

    def visit_text_part_2(self, node, visited_children):
        return node_nonempty(node, visited_children)

    def visit_intro_si_clause(self, node, visited_children):
        return node_nonempty(node, visited_children)

    def visit_faho_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_text_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_paragraphs(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_paragraph(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_statement(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_statement_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_statement_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_statement_3(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_fragment(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_prenex(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sentence(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sentence_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sentence_start(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_subsentence(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bridi_tail(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bridi_tail_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bridi_tail_start(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bridi_tail_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bridi_tail_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bridi_tail_3(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_gek_sentence(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_tail_terms(self, node, visited_children):
        return node_nonempty(node, visited_children)

    def visit_terms(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_terms_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_terms_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_nonabs_terms(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_nonabs_terms_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_nonabs_terms_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_pehe_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_cehe_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_term(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_term_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_abs_term(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_abs_term_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_abs_tag_term(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_term_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_term_start(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_termset(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_gek_termset(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_terms_gik_terms(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_nonabs_termset(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_nonabs_gek_termset(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_nonabs_terms_gik_terms(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti_3(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti_4(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti_5(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti_6(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_li_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti_tail(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_sumti_tail_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_relative_clauses(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_relative_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_relative_clause_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_relative_clause_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_relative_clause_start(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_selbri(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_selbri_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_selbri_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_selbri_3(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_selbri_4(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_selbri_5(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_selbri_6(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_tanru_unit(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_tanru_unit_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_tanru_unit_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_linkargs(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_linkargs_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_linkargs_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_linkargs_start(self, node, visited_children):
        return node_simple_alias(node, visited_children)

    def visit_links(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_links_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_links_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_links_start(self, node, visited_children):
        return node_simple_alias(node, visited_children)

    def visit_quantifier(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_mex(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_mex_0(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_mex_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_mex_start(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_rp_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_mex_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_mex_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    # mex_forethought

    def visit_fore_operands(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_rp_expression(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_rp_expression_tail(self, node, visited_children):
        # emulate () in camxes-ilmen right-recursive rule
        if visited_children == "":
            visited_children = []
        elif isinstance(visited_children, list) and visited_children[-1] == "":
            visited_children[-1] = []
        return camxes_node(node, visited_children)

    def visit_operator(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operator_0(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operator_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operator_start(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operator_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operator_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_mex_operator(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operand(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operand_0(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operand_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operand_start(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operand_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operand_2(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_operand_3(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_number(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_lerfu_string(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_lerfu_word(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_ek(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_gihek(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_gihek_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_gihek_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_jek(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_joik(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_interval(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_joik_ek(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_joik_ek_1(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_joik_ek_sa(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_joik_jek(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_gek(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_guhek(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_gik(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_tag(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_stag(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_tense_modal(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_simple_tense_modal(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_time(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_time_offset(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_space(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_space_offset(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_space_interval(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_space_int_props(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_interval_property(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_free(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_xi_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_vocative(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_indicators(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_indicator(self, node, visited_children):
        children = _children(node, visited_children)
        return camxes_node(node, children[0]) # expr doesn't include [1]

    # Magic Words

    def visit_zei_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_zei_clause_no_pre(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bu_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bu_clause_no_pre(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_zei_tail(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_bu_tail(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_pre_zei_bu(self, node, visited_children):
        return camxes_node(node, visited_children)

    # dot_star

    def visit_post_clause(self, node, visited_children):
        return node_nonempty(node, visited_children)

    # pre_clause

    def visit_any_word_SA_handling(self, node, visited_children):
        return camxes_node(node, visited_children)

    # known_cmavo_SA

    # ___ SPACE ___

    # su_clause

    # si_clause

    def visit_erasable_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    # sa_word

    # si_word

    # su_word

    # ___ ELIDIBLE TERMINATORS ___

    def visit_BEhO_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_BOI_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_CU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_DOhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_FEhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_GEhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_KEI_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_KEhE_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_KU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_KUhE_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_KUhO_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_LIhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_LOhO_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_LUhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_MEhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_NUhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_SEhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_TEhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_TOI_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_TUhU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_VAU_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    def visit_VEhO_elidible(self, node, visited_children):
        return node_elidible(node, visited_children)

    # ___ SELMAHO ___

    def visit_BRIVLA_clause(self, node, visited_children):
        children = _children(node, visited_children)
        if len(children) == 2:
            return _node2(node.expr_name, children[0], children[1])
        else:
            return _camxes_node(node.expr_name, children[0])

    # BRIVLA_pre
    # BRIVLA_post
    # ...

    def visit_CMEVLA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_CMAVO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_A_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BAI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BAhE_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_BE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BEI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BEhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BIhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BIhI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_BY_clause(self, node, visited_children):
        children = _children(node, visited_children)
        if children[0] == "bu_clause":
            return _node_simple(node.expr_name, children)
        else:
            return _node2(node.expr_name, children[0], children[1])

    def visit_CAhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_CAI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_CEI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_CEhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_CO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_COI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_CU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_CUhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_DAhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_DOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_DOhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FAhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FAhO_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_FEhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FEhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FIhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FUhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FUhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_FUhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_GA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_GAhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_GEhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_GI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_GIhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_GOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_GOhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_GUhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_I_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_JA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_JAI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_JOhI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_JOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_KE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_KEhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_KEI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_KI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_KOhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_KU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_KUhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_KUhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LAU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LAhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LEhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LIhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LOhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LOhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_LUhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_MAhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_MAI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ME_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_MEhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_MOhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_MOhI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_MOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NAI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NAhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NAhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NIhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NIhO_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_NOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NUhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NUhI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_NUhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_PA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_PEhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_PEhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_PU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_RAhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ROI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_SA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_SE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_SEI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_SEhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_SI_clause(self, node, visited_children):
        return camxes_node(node, visited_children)

    def visit_SOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_SU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_TAhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_TEhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_TEI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_TO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_TOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_TUhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_TUhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_UI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_VA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_VAU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_VEI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_VEhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_VUhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_VEhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_VIhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_VUhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_XI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ZAhO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ZEhA_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ZEI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ZI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ZIhE_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ZO_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ZOI_clause(self, node, visited_children):
        return node2(node, visited_children)

    def visit_ZOhU_clause(self, node, visited_children):
        return node2(node, visited_children)

    # ___ MORPHOLOGY ___

    def visit_CMEVLA(self, node, visited_children):
        return node_simple_alias(node, visited_children)

    def visit_BRIVLA(self, node, visited_children):
        return node_simple(node, visited_children)

    def visit_gismu_2(self, node, visited_children):
        return node_simple_alias(node, visited_children, "gismu")

    def visit_CMAVO(self, node, visited_children):
        return node_simple(node, visited_children)

    # ___ GRAMMAR ___

    # lojban_word

    def visit_any_word(self, node, visited_children):
        return indexed(node, visited_children, 0)

    def visit_zoi_open(self, node, visited_children):
        delimiter = visited_children[1]
        return terminal(delimiter)

    def visit_zoi_word(self, node, visited_children):
        return terminal("")

    # zoi_close

    # ____

    def visit_cmevla(self, node, visited_children):
        return join_named(node, visited_children)

    # ____

    def visit_cmavo(self, node, visited_children):
        return join(node, visited_children)

    def visit_CVCy_lujvo(self, node, visited_children):
        return join(node, visited_children)

    def visit_cmavo_form(self, node, visited_children):
        return join(node, visited_children)

    # ____

    def visit_brivla(self, node, visited_children):
        return join(node, visited_children)

    def visit_brivla_core(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_initial_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_initial_rafsi(self, node, visited_children):
        return join(node, visited_children)

    # ____

    def visit_any_extended_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_fuhivla(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_extended_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_extended_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_brivla_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_brivla_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_fuhivla_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_fuhivla_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_fuhivla_head(self, node, visited_children):
        return join(node, visited_children)

    def visit_brivla_head(self, node, visited_children):
        return join(node, visited_children)

    def visit_slinkuhi(self, node, visited_children):
        return join(node, visited_children)

    def visit_rafsi_string(self, node, visited_children):
        return join(node, visited_children)

    # ____

    def visit_gismu(self, node, visited_children):
        return join(node, visited_children)

    def visit_CVV_final_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_short_final_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_y_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_y_less_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_long_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_CVC_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_CCV_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_CVV_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_y_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_y_less_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_long_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_CVC_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_CCV_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_CVV_rafsi(self, node, visited_children):
        return join(node, visited_children)

    def visit_r_hyphen(self, node, visited_children):
        return join(node, visited_children)

    # ____

    def visit_final_syllable(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_syllable(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_diphthong(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed_vowel(self, node, visited_children):
        return join(node, visited_children)

    def visit_unstressed_syllable(self, node, visited_children):
        return join(node, visited_children)

    def visit_unstressed_diphthong(self, node, visited_children):
        return join(node, visited_children)

    def visit_unstressed_vowel(self, node, visited_children):
        return join(node, visited_children)

    def visit_stress(self, node, visited_children):
        return join(node, visited_children)

    def visit_stressed(self, node, visited_children):
        return join(node, visited_children)

    def visit_any_syllable(self, node, visited_children):
        return join(node, visited_children)

    def visit_syllable(self, node, visited_children):
        return join(node, visited_children)

    def visit_consonantal_syllable(self, node, visited_children):
        return join(node, visited_children)

    def visit_coda(self, node, visited_children):
        return join(node, visited_children)

    def visit_onset(self, node, visited_children):
        return join(node, visited_children)

    def visit_nucleus(self, node, visited_children):
        return join(node, visited_children)

    # ____

    # glide

    def visit_diphthong(self, node, visited_children):
        return join(node, visited_children)

    # vowel

    def visit_a(self, node, visited_children):
        return terminal("a")

    def visit_e(self, node, visited_children):
        return terminal("e")

    def visit_i(self, node, visited_children):
        return terminal("i")

    def visit_o(self, node, visited_children):
        return terminal("o")

    def visit_u(self, node, visited_children):
        return terminal("u")

    def visit_y(self, node, visited_children):
        return terminal("y")

    # ____

    def visit_cluster(self, node, visited_children):
        return join(node, visited_children)

    def visit_initial_pair(self, node, visited_children):
        return join(node, visited_children)

    def visit_initial(self, node, visited_children):
        return join(node, visited_children)

    def visit_affricate(self, node, visited_children):
        return join(node, visited_children)

    def visit_liquid(self, node, visited_children):
        return join(node, visited_children)

    def visit_other(self, node, visited_children):
        return join(node, visited_children)

    def visit_sibilant(self, node, visited_children):
        return join(node, visited_children)

    # ...

    def visit_l(self, node, visited_children):
        return terminal("l")

    def visit_m(self, node, visited_children):
        return terminal("m")

    def visit_n(self, node, visited_children):
        return terminal("n")

    def visit_r(self, node, visited_children):
        return terminal("r")

    def visit_b(self, node, visited_children):
        return terminal("b")

    def visit_d(self, node, visited_children):
        return terminal("d")

    def visit_g(self, node, visited_children):
        return terminal("g")

    def visit_v(self, node, visited_children):
        return terminal("v")

    def visit_j(self, node, visited_children):
        return terminal("j")

    def visit_z(self, node, visited_children):
        return terminal("z")

    def visit_s(self, node, visited_children):
        return terminal("s")

    def visit_c(self, node, visited_children):
        return terminal("c")

    def visit_x(self, node, visited_children):
        return terminal("x")

    def visit_k(self, node, visited_children):
        return terminal("k")

    def visit_f(self, node, visited_children):
        return terminal("f")

    def visit_p(self, node, visited_children):
        return terminal("p")

    def visit_t(self, node, visited_children):
        return terminal("t")

    def visit_h(self, node, visited_children):
        return terminal("'")

    # ____

    def visit_digit(self, node, visited_children):
        return join(node, visited_children)

    def visit_post_word(self, node, visited_children):
        return join(node, visited_children)

    def visit_pause(self, node, visited_children):
        return join(node, visited_children)

    def visit_EOF(self, node, visited_children):
        return join(node, visited_children)

    def visit_comma(self, node, visited_children):
        return terminal("")

    def visit_non_lojban_word(self, node, visited_children):
        return join(node, visited_children)

    def visit_non_space(self, node, visited_children):
        return join(node, visited_children)

    def visit_space_char(self, node, visited_children):
        return terminal("")

    # ____

    def visit_spaces(self, node, visited_children):
        return join(node, visited_children)

    def visit_initial_spaces(self, node, visited_children):
        return join(node, visited_children)

    def visit_ybu(self, node, visited_children):
        return _node_name(node)

    def visit_lujvo(self, node, visited_children):
        return join_named(node, visited_children)

    # ____

    def visit_A(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BAI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BAhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BEI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BEhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BIhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BIhI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_BY(self, node, visited_children):
        children = _children(node, visited_children)
        return _join_named(node.expr_name, children[1]) # skip lookahead

    def visit_CAhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_CAI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_CEI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_CEhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_CO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_COI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_CU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_CUhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_DAhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_DOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_DOhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FAhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FAhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FEhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FEhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FIhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FUhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FUhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_FUhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_GA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_GAhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_GEhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_GI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_GIhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_GOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_GOhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_GUhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_I(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_JA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_JAI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_JOhI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_JOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_KE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_KEhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_KEI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_KI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_KOhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_KU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_KUhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_KUhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LAU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LAhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LEhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LIhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LOhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LOhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_LUhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_MAhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_MAI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ME(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_MEhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_MOhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_MOhI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_MOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NAI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NAhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NAhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NIhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NIhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NUhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NUhI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_NUhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_PA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_PEhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_PEhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_PU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_RAhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ROI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_SA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_SE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_SEI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_SEhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_SI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_SOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_SU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_TAhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_TEhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_TEI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_TO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_TOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_TUhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_TUhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_UI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_VA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_VAU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_VEI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_VEhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_VUhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_VEhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_VIhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_VUhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_XI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_Y(self, node, visited_children):
        return join_indexed_children(node, visited_children, 1)

    def visit_ZAhO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ZEhA(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ZEI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ZI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ZIhE(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ZO(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ZOI(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    def visit_ZOhU(self, node, visited_children):
        return join_indexed(node, visited_children, 1)

    ####

    def generic_visit(self, node, visited_children):
        return default(node, visited_children)

