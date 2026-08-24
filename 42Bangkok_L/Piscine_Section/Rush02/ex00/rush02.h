/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush02.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ataweech <ataweech@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 20:10:00 by ataweech          #+#    #+#             */
/*   Updated: 2026/07/26 21:07:04 by ataweech         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef RUSH02_H
# define RUSH02_H

# include <fcntl.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_list
{
	char			*key;
	char			*value;
	struct s_list	*next;
}	t_list;

void	ft_putstr(char *str);
int		ft_strlen(char *str);
char	*ft_strdup(char *src);
int		input_validation(int argc, char **argv);

t_list	*create_node(char *key, char *value);
void	ft_lstadd_back(t_list **lst, t_list *new_node);
char	*get_value(t_list *head, char *key);
void	free_list(t_list *head);

t_list	*parse_dict(char *filename);

void	get_chunk(char *str, int g, int g_count, char *chunk);
int		check_chunk_keys(char *chunk, t_list *dict);
int		validate_all_keys(char *num_str, t_list *dict, int group_count);
char	*get_multiplier(int magnitude);
void	print_word(char *word, int *first_word);
int		handle_zero(t_list *dict);
void	print_chunk(char *chunk, t_list *dict, int *first);
int		convert_number(char *num_str, t_list *dict);

#endif