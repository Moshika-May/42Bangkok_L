/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_boolean.h                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mbury <mbury@student.42bangkok.com>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/23 10:41:07 by mbury             #+#    #+#             */
/*   Updated: 2026/07/23 11:16:41 by mbury            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_BOOLEAN_H
# define FT_BOOLEAN_H
# define EVEN ft_check_even
# define EVEN_MSG "I have an even number of arguments."
# define ODD_MSG "I have an odd number of arguments."
# define SUCCESS 0
# define TRUE 1
# define FALSE 0
# include <unistd.h>

int	ft_check_even(int nbr)
{
	if (nbr % 2 == 0)
		return (1);
	else
		return (0);
}
typedef int	t_bool;

#endif // FT_BOOLEAN_H
