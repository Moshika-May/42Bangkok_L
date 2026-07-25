/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hzheng2 <hzheng2@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 17:37:20 by hzheng2           #+#    #+#             */
/*   Updated: 2026/07/25 11:07:53 by hzheng2          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdlib.h>

int	getlen(char *str)
{
	int	len;

	len = 0;
	while (*str != '\0')
	{
		len++;
		str++;
	}
	return (len);
}

int	getalllen(int size, char **str)
{
	int	len;
	int	idx1;

	len = 0;
	idx1 = 0;
	while (idx1 < size)
	{
		len += getlen(str[idx1]);
		idx1++;
	}
	return (len);
}

void	putstr(char *dest, char *src, int *idx)
{
	while (*src != '\0')
	{
		*dest = *src;
		src++;
		dest++;
		(*idx)++;
	}
}

char	*ft_strjoin(int size, char **strs, char *sep)
{
	int		idx1;
	int		len;
	int		idxans;
	char	*ans;

	idx1 = 0;
	idxans = 0;
	if (size <= 0)
	{
		ans = malloc(sizeof(char) * 1);
		ans[0] = '\0';
		return (ans);
	}
	len = (getlen(sep) * (size - 1) + getalllen(size, strs) + 1);
	ans = malloc(sizeof(char) * len);
	while (idx1 < size)
	{
		putstr(ans + idxans, *(strs + idx1), &idxans);
		if (idx1 != size - 1)
			putstr(ans + idxans, sep, &idxans);
		idx1++;
	}
	*(ans + idxans) = '\0';
	return (ans);
}
/*
#include <stdio.h>
int		main(int argc, char **argv)
{
	char *ans;

	ans = ft_strjoin(argc - 1,++argv,"  step  ");
	printf("%s" ,ans);
	return 0;
}*/