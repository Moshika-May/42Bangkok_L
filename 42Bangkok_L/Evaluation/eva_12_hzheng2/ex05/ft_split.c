/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hzheng2 <hzheng2@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/24 20:04:29 by hzheng2           #+#    #+#             */
/*   Updated: 2026/07/25 12:54:00 by hzheng2          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	isinarr(char *charset, char c)
{
	int	idx;

	idx = 0;
	while (*(charset + idx) != '\0')
	{
		if (*(charset + idx) == c)
			return (1);
		idx++;
	}
	return (0);
}

int	countallword(char *str, char *charset)
{
	int	ans;
	int	isfoundword;

	ans = 0;
	isfoundword = 0;
	while (*str != '\0')
	{
		if (isinarr(charset, *str) == 1)
		{
			if (isfoundword == 1)
				ans++;
			isfoundword = 0;
		}
		else
		{
			isfoundword = 1;
		}
		str++;
	}
	if (isfoundword == 1)
		ans++;
	return (ans);
}

int	*getans(char *str, char *charset, int len)
{
	int	*ans;
	int	isfoundword;
	int	idxans;
	int	idx;

	ans = malloc(sizeof(int) * len);
	isfoundword = 0;
	idxans = 0;
	idx = 0;
	while (*(str + idx) != '\0')
	{
		if (isinarr(charset,*(str + idx)) == 1)
		{
			isfoundword = 0;
		}
		else
		{
			if (isfoundword == 0)
				ans[idxans++] = idx;
			isfoundword = 1;
		}
		idx++;
	}
	return (ans);
}

int	getlen(char *str, char *charset)
{
	int	len;

	len = 1;
	while (isinarr(charset,*str) == 0 && *str != '\0')
	{
		len++;
		str++;
	}
	return (len);
}

char	**ft_split(char *str, char *charset)
{
	char	**ans;
	int		*ansidx;
	int		len;
	int		idx;
	int		idx2;

	len = countallword(str, charset);
	ans = malloc(sizeof(char *) * (len + 1));
	ansidx = getans(str, charset, len);
	idx = 0;
	while (idx < len)
	{
		idx2 = 0;
		ans[idx] = malloc(sizeof(char) * getlen(str + ansidx[idx], charset));
		while (str[ansidx[idx] + idx2] != '\0'
			&& isinarr(charset, str[ansidx[idx] + idx2]) == 0)
		{
			ans[idx][idx2] = str[ansidx[idx] + idx2];
			idx2++;
		}
		ans[idx][idx2] = '\0';
		idx++;
	}
	ans[idx] = 0;
	return (ans);
}
/*
#include <stdio.h>
int		main(int argc, char **argv)
{
	char **ans;
	int idx;

	idx = 0;
	ans = ft_split(argv[1]," ");
	while (*ans != (void *)0)
	{
		printf("%s\n" ,*(ans++));
	}
	return 0;
}*/