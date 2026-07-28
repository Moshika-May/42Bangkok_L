/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_convert_base.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/26 13:26:13 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/28 22:50:53 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdlib.h>

int			base_check_n_len(char *base);
int			index_base(char c, char *base);
char		*ft_itoa_base(long long nbr, char *base);

long long	ft_atoi_base(char *str, char *base)
{
	unsigned int	i;
	int				j;
	long long		k;
	int				b_len;

	i = 0;
	j = 1;
	k = 0;
	b_len = base_check_n_len(base);
	if (!b_len)
		return (0);
	while (str[i] == ' ' || (str[i] >= '\t' && str[i] <= '\r'))
		i++;
	while (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			j = -j;
		i++;
	}
	while (str[i] && index_base(str[i], base) != -1)
		k = (k * b_len) + index_base(str[i++], base);
	return (k * j);
}

char	*ft_convert_base(char *nbr, char *base_from, char *base_to)
{
	long long	n;

	if (!nbr || !base_check_n_len(base_from) || !base_check_n_len(base_to))
		return (NULL);
	n = ft_atoi_base(nbr, base_from);
	return (ft_itoa_base(n, base_to));
}
/*
#include <stdio.h>

int	main(int c, char **vec)
{
	char	*after;

	after = ft_convert_base(vec[1], vec[2], vec[3]);
	if (c != 4)
		return (0);
	printf("Num B: %s\n", vec[1]);
	printf("From: %s\n", vec[2]);
	printf("To: %s\n", vec[3]);
	printf("Num A: %s\n", after);
	free(after);
	return (0);
}
*/
