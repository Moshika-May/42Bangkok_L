/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ll_helper.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 19:49:12 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 20:49:44 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush02.h"

t_list	*create_node(char *key, char *value)
{
	t_list	*node;

	node = malloc(sizeof(t_list));
	if (!node)
		return (NULL);
	node->key = ft_strdup(key);
	node->value = ft_strdup(value);
	node->next = NULL;
	return (node);
}

void	ft_lstadd_back(t_list **lst, t_list *new_node)
{
	t_list	*curr;

	if (!lst || !new_node)
		return ;
	if (*lst == NULL)
	{
		*lst = new_node;
		return ;
	}
	curr = *lst;
	while (curr->next)
		curr = curr->next;
	curr->next = new_node;
}

char	*get_value(t_list *head, char *key)
{
	int	i;

	while (head)
	{
		i = 0;
		while (head->key[i] && key[i] && head->key[i] == key[i])
			i++;
		if (head->key[i] == '\0' && key[i] == '\0')
			return (head->value);
		head = head->next;
	}
	return (NULL);
}

void	free_list(t_list *head)
{
	t_list	*tmp;

	while (head)
	{
		tmp = head->next;
		if (head->key)
			free(head->key);
		if (head->value)
			free(head->value);
		free(head);
		head = tmp;
	}
}
