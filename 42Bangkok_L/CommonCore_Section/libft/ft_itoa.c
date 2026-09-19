/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/13 00:20:07 by kmahanin          #+#    #+#             */
/*   Updated: 2026/09/19 15:26:49 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	int_len(int n)
{
	size_t	i;
	long	j;
	int		sign;

	i = 0;
	j = n;
	sign = 1;
	if (n == 0)
		return (1);
	if (n < 0)
	{
		j = -j;
		sign = -sign;
		i++;
	}
	while (j > 0)
	{
		j /= 10;
		i++;
	}
	return (i);
}

static char	*convert(int n, char *a, size_t len)
{
	size_t	i;
	long	j;

	j = n;
	i = len;
	a[i] = '\0';
	if (j < 0)
	{
		a[0] = '-';
		j = -j;
	}
	while (i > (n < 0))
	{
		a[i - 1] = (j % 10) + '0';
		j /= 10;
		i--;
	}
	return (a);
}

char	*ft_itoa(int n)
{
	size_t	len;
	char	*a;

	len = int_len(n);
	a = malloc(sizeof(char) * (len + 1));
	if (!a)
		return (NULL);
	return (convert(n, a, len));
}
/*
#include <stdio.h>
#include <string.h>

int	main(int ac, char **av)
{
	char	*str;

	(void)ac;
	str = ft_itoa(atoi(av[1]));
	printf("%s\n", str);
	free(str);
	return (0);
}
*/
/*
char	*ft_itoa_base(long long nbr, char *base)
{
	long long		n;
	unsigned int	b_len;
	unsigned int	i;
	char			*arr;

	b_len = base_check_n_len(base);
	n = nbr;
	i = get_num_len(n, b_len);
	arr = (char *)malloc(sizeof(char) * (i + 1));
	if (!arr)
		return (NULL);
	arr[i] = '\0';
	if (n == 0)
		arr[0] = base[0];
	if (n < 0)
	{
		arr[0] = '-';
		n = -n;
	}
	while (n > 0)
	{
		arr[--i] = base[n % b_len];
		n /= b_len;
	}
	return (arr);
}
*/
