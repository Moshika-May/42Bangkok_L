/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   helper_func.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: kmahanin <kmahanin@student.42bangkok.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/24 22:39:22 by kmahanin          #+#    #+#             */
/*   Updated: 2026/07/25 00:03:57 by kmahanin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

unsigned long long	atoull(char *str)
{
	unsigned long long	var;
	unsigned int		i;

	var = 0;
	i = 0;
	while (str[i] == ' ' || (str[i] >= '\t' && str[i] <= '\r'))
		i++;
	while (str[i] >= '0' && str[i] <= '9')
	{
		var = (var * 10) + (str[i] - '0');
		i++;
	}
	return (var);
}

int	len(char *str)
{
	unsigned int	i;

	i = 0;
	while (str && str[i])
		i++;
	return (i);
}
/* Use I guess ?
char	*strdup(char *src)
{
	unsgined int	i;
	char			*dest;

	i = 0;
	dest = malloc(sizeof(char) * (len(src) + 1));
	if (!dest)
		return (0);
	while (src[i])
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}
*/
