/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rsh02.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/24 21:46:42 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/27 14:39:15 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef RSH02_H
# define RSH02_H

# include <fcntl.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_dict
{
	unsigned __int128	nb;
	char				*val;
}						t_dict;

int						input_validation(int argc, char **argv);
void					putstr(char *str);
int						len(char *str);
unsigned __int128		atoull(char *str);
char					*ft_strdup(char *src);
char					*get_dict_contact(char *path);

t_dict					*parse_dict(char *path);
void					free_dict(t_dict *dict);
void					sort_dict(t_dict *dict, int size);

void					convert_number(unsigned __int128 n, t_dict *dict,
							int *first);
#endif
