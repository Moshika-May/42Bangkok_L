/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bsq.h                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 15:46:05 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/29 17:35:16 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef BSQ_H
# define BSQ_H

# include <fcntl.h>
# include <stdlib.h>
# include <unistd.h>

char	*finalize_line(char *buf, int len, char c);
char	*read_line(int fd);
int		parse_header(int fd, int *m, char *cfg);
int		read_grid(int fd, char **grid, int *dim, char *cfg);
int		**alloc_dp(int m, int n);
void	free_dp(int **dp, int m);
int		min2(int a, int b);
int		min3(int a, int b, int c);
int		ft_atoi(char *str);
void	print_and_free(char **grid, int m, int n);
int		is_valid_cfg(char *cfg);
int		check_line(char *line, int n, char *cfg);
void	fill_bsq(char **grid, int *max, char fill);
void	compute_cell(int **dp, char **g, char *cfg, int *c);
void	bsq(char **grid, int m, int n, char *cfg);
void	process_file(int fd);

#endif
