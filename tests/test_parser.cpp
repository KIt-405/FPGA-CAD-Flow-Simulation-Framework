#include "parse/ast_node.hpp"
#include <iostream>
#include <cassert>
#include <string>

// Helper to check node types safely
void assert_node(const ASTNode* node, NodeType expected_type, const std::string& expected_name = "") {
    assert(node != nullptr);
    assert(node->type == expected_type);
    if (expected_type == NodeType::VAR) {
        assert(node->name == expected_name);
    }
}

void test_basic_parsing() {
    std::cout << "[Test] Running test_basic_parsing..." << std::endl;
    auto root = parse_rtl("A AND B");
    
    assert_node(root.get(), NodeType::AND);
    assert_node(root->left.get(), NodeType::VAR, "A");
    assert_node(root->right.get(), NodeType::VAR, "B");
}

void test_operator_precedence() {
    std::cout << "[Test] Running test_operator_precedence (A OR B AND C)..." << std::endl;
    // AND should be deeper in the tree than OR
    auto root = parse_rtl("A OR B AND C");
    
    assert_node(root.get(), NodeType::OR);
    assert_node(root->left.get(), NodeType::VAR, "A");
    assert_node(root->right.get(), NodeType::AND);
    
    auto and_node = root->right.get();
    assert_node(and_node->left.get(), NodeType::VAR, "B");
    assert_node(and_node->right.get(), NodeType::VAR, "C");
}

void test_parentheses_override() {
    std::cout << "[Test] Running test_parentheses_override ((A OR B) AND C)..." << std::endl;
    // Parentheses should force OR to be deeper than AND
    auto root = parse_rtl("(A OR B) AND C");
    
    assert_node(root.get(), NodeType::AND);
    assert_node(root->left.get(), NodeType::OR);
    assert_node(root->right.get(), NodeType::VAR, "C");
}

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "  Starting Front-End AST Parser Tests   " << std::endl;
    std::cout << "========================================" << std::endl;

    test_basic_parsing();
    test_operator_precedence();
    test_parentheses_override();

    std::cout << "\n[SUCCESS] All AST Parser tests passed!" << std::endl;
    return 0;
}
