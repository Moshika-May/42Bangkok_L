/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_convert_base.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hzheng2 <hzheng2@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 14:18:46 by hzheng2           #+#    #+#             */
/*   Updated: 2026/07/25 11:03:36 by hzheng2          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdlib.h>

int	get_size(char *arr);
int	get_idx(char c, char *arr);
int	isbasevalid(char *base);

int	ft_atoi_base(char *str, char *base_from)
{
	int	sign;
	int	result;
	int	base_len;
	int	digit_val;

	sign = 1;
	result = 0;
	base_len = get_size(base_from);
	while (*str == ' ' || (*str >= 9 && *str <= 13))
		str++;
	while (*str == '-' || *str == '+')
	{
		if (*str == '-')
			sign *= -1;
		str++;
	}
	while (*str)
	{
		digit_val = get_idx(*str, base_from);
		if (digit_val == -1)
			break ;
		result = (result * base_len) + digit_val;
		str++;
	}
	return (result * sign);
}

int	get_num_length(long num, int base_len)
{
	int	len;

	len = 0;
	if (num <= 0)
	{
		len++;
		num = -num;
	}
	while (num > 0)
	{
		num /= base_len;
		len++;
	}
	return (len);
}

char	*createans(long num, char *base_to, int base_len)
{
	int		str_len;
	char	*ans;

	str_len = get_num_length(num, base_len);
	ans = malloc(sizeof(char) * (str_len + 1));
	if (!ans)
		return (NULL);
	ans[str_len] = '\0';
	if (num == 0)
	{
		ans[0] = base_to[0];
		return (ans);
	}
	if (num < 0)
	{
		ans[0] = '-';
		num = -num;
	}
	while (num > 0)
	{
		ans[--str_len] = base_to[num % base_len];
		num /= base_len;
	}
	return (ans);
}

char	*ft_convert_base(char *nbr, char *base_from, char *base_to)
{
	long	num;
	int		base_len;

	if (!nbr || !base_from || !base_to)
		return (NULL);
	if (!isbasevalid(base_from) || !isbasevalid(base_to))
		return (NULL);
	num = ft_atoi_base(nbr, base_from);
	base_len = get_size(base_to);
	return (createans(num, base_to, base_len));
}
/*
#include <stdio.h>
int	main(int ar, char **argv)
{
	char	*ans;

	if (argc == 4)
	{
		ans = ft_convert_base(argv[1], argv[2], argv[3]);
		if (ans)
		{
			printf("%s\n", ans);
			free(ans);
		}
	}
	return (0);
}*/